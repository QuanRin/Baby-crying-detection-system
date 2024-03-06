import torch
from torch.utils.data import DataLoader
from .model import CNNNetwork, AlexNet
from dataset import CryDataset
from train import mel_spectrogram, step
import os
from sklearn.metrics import precision_score
from .audio_utils import CLASS_MAPPING, NUM_CLASSES


def predict(model, input, target):
    model.eval()
    with torch.no_grad():
        predictions = model(input)
        predicted_index = predictions[0].argmax(0)
        if predicted_index < 0 or predicted_index >= NUM_CLASSES:
            print("Predicted index is out of range.")
            return None
        return predicted_index.item(), target.item()


model = AlexNet(num_classes=NUM_CLASSES)
state_dict = torch.load(os.path.join(os.path.dirname(
    __file__), "cnnnet.pth"), map_location=torch.device('cpu'))
model.load_state_dict(state_dict)


def predict_one(waveform, CLASS_MAPPING=CLASS_MAPPING):
    model.eval()
    input = mel_spectrogram(waveform).unsqueeze(0)
    with torch.no_grad():
        predictions = model(input)
        print(predictions)
        predicted_index = predictions[0].argmax(0)
        if predicted_index < 0 or predicted_index >= NUM_CLASSES:
            print("Predicted index is out of range.")
            return None
        predicted = CLASS_MAPPING[predicted_index]
    return predicted


if __name__ == "__main__":
    # load back the model
    cnn = AlexNet(num_classes=NUM_CLASSES)
    state_dict = torch.load("cnnnet.pth")
    cnn.load_state_dict(state_dict)

    ds = CryDataset(mel_spectrogram, device="cpu", csv_path='test_data.csv')

    batch_size = 1
    data_loader = DataLoader(ds, batch_size=batch_size, shuffle=False)

    # Initialize variables to accumulate TP, FP, and FN
    y_true = []
    y_pred = []

    for batch in data_loader:
        inputs, targets = batch

        for i in range(len(inputs)):
            input = inputs[i].unsqueeze(0)
            predicted_index, target_index = predict(cnn, input, targets[i])

            # Append true labels and predicted labels
            y_true.append(target_index)
            y_pred.append(predicted_index)

            # predicted = CLASS_MAPPING[predicted_index]
            # expected = CLASS_MAPPING[target_index]
            # print(f"Predicted: '{predicted}', Expected: '{expected}'")

    # Calculate precision for each class
    precision = precision_score(y_true, y_pred, average=None)

    for i, class_precision in enumerate(precision):
        print(f'Precision for class {CLASS_MAPPING[i]}: {class_precision}')
