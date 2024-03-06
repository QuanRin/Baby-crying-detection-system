import matplotlib.pyplot as plt
import os
import torchaudio
from audio_utils import SAMPLE_RATE, HOP_LEN, WIN_LEN, N_MELS
import torch

# Load the raw audio file
raw_wav, sr = torchaudio.load(os.path.join(
    os.path.dirname(__file__), 'clean', 'Silence', 'silence.wav_1_0.wav'))

# Create a MelSpectrogram transform
mfcc_transform = torchaudio.transforms.MFCC(
    sample_rate=SAMPLE_RATE,
    n_mfcc=24,
    melkwargs={'n_fft': 1024,
               'hop_length': HOP_LEN,
               'win_length': WIN_LEN,
               'n_mels': N_MELS,
               'window_fn': torch.hamming_window}
)

# # Apply the transform to the raw audio
# mel_spectrogram = mel_transform(raw_wav)

# # Convert to decibels
# mel_spectrogram_db = torchaudio.transforms.AmplitudeToDB()(mel_spectrogram)

# # Plot the Mel spectrogram
# plt.figure(figsize=(12, 4))
# plt.imshow(mel_spectrogram_db[0].numpy(),
#            cmap='viridis', aspect='auto', origin='lower')
# plt.title('Mel Spectrogram')
# plt.xlabel('Time')
# plt.ylabel('Mel Filter')
# plt.colorbar(format='%+2.0f dB')
# plt.show()

mfcc = mfcc_transform(raw_wav)

# Convert the MFCC tensor to a NumPy array
mfcc_np = mfcc.numpy()

# Plot the MFCC spectrogram
plt.figure(figsize=(10, 4))
plt.imshow(mfcc_np[0].T, aspect='auto', origin='lower', cmap='viridis')

plt.title('MFCC Spectrogram')
plt.xlabel('Time')
plt.ylabel('MFCC Coefficients')
plt.colorbar(format='%+2.0f dB')
plt.show()
