import matplotlib.pyplot as plt
import torchaudio
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio.wav')


# waveform = torch.tensor(waveform).reshape(2, -1)


waveform, sample_rate = torchaudio.load(path)

# plt.plot(waveform.t().numpy())
# plt.show()
print(waveform.size(1))
