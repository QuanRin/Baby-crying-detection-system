import os
import random
import torch
import torchaudio
from torch import nn
from torchaudio import transforms

SAMPLE_RATE = 16000
DELTA_TIME = 5
CLASS_MAPPING = [
    "Cry",
    "Other"
]
NUM_CLASSES = len(CLASS_MAPPING)
BATCH_SIZE = 64
EPOCHS = 101
LEARNING_RATE = 0.00001
N_MELS = 64
NFFT = 2048
N_MFCC = 24
HOP_LEN = int(10*(10**-3)*SAMPLE_RATE)
WIN_LEN = int(30*(10**-3)*SAMPLE_RATE)
WIN_FN = torch.hamming_window

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"


class AudioUtil():
    @staticmethod
    def time_shift(sig, shift_limit):
        _, sig_len = sig.shape
        shift_amt = int(random.random() * shift_limit * sig_len)
        return sig.roll(shift_amt)

    @staticmethod
    def spectro_gram():
        spectrogram = torchaudio.transforms.MelSpectrogram(
            sample_rate=SAMPLE_RATE,
            n_fft=NFFT,
            hop_length=HOP_LEN,
            win_length=WIN_LEN,
            n_mels=N_MELS,
            window_fn=WIN_FN
        )

        return (spectrogram)

    @staticmethod
    def spectro_augment(spec, max_mask_pct=0.1, n_freq_masks=1, n_time_masks=1):
        _, n_mels, n_steps = spec.shape
        mask_value = spec.mean()
        aug_spec = spec

        freq_mask_param = max_mask_pct * n_mels
        for _ in range(n_freq_masks):
            aug_spec = transforms.FrequencyMasking(
                freq_mask_param)(aug_spec, mask_value)

        time_mask_param = max_mask_pct * n_steps
        for _ in range(n_time_masks):
            aug_spec = transforms.TimeMasking(
                time_mask_param)(aug_spec, mask_value)

        return aug_spec

# Model used


class VGGish(nn.Module):
    """Based on:
        https://github.com/harritaylor/torchvggish/blob/master/docs/_example_download_weights.ipynb
    """

    def __init__(self, num_classes: int):  # Added num_classes
        super(VGGish, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 64, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(128, 256, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(256, 512, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.AdaptiveMaxPool2d((4, 6)))  # Replaced: MaxPool2d(2,2)
        self.embeddings = nn.Sequential(
            nn.Linear(512*24, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, 128),
            nn.ReLU(inplace=True))
        self.head = nn.Linear(128, num_classes)  # Added
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.embeddings(x)
        x = self.head(x)  # Added
        x = self.softmax(x)
        return x


model = None


def _load_model(path="audionet.70.pth"):
    global model
    model = VGGish(num_classes=NUM_CLASSES).to(device=device)
    state_dict = torch.load(os.path.join(os.path.dirname(
        __file__), path), map_location=torch.device(device))
    model.load_state_dict(state_dict)
    return model


def predict_one(waveform, CLASS_MAPPING=CLASS_MAPPING):
    global model
    if model == None:
        model = _load_model()
    model.eval()
    input = torchaudio.transforms.AmplitudeToDB(top_db=80)(
        AudioUtil.spectro_gram()(waveform)).unsqueeze(0).to(device)
    with torch.no_grad():
        predictions = model(input)
        predicted_index = predictions[0].argmax(0)
        if predicted_index < 0 or predicted_index >= NUM_CLASSES:
            print("Predicted index is out of range.")
            return None
        predicted = CLASS_MAPPING[predicted_index]
    print(predictions)
    return predicted, predictions[0][predicted_index].item()
