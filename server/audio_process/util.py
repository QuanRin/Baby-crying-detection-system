import random
from torchaudio import transforms
import torchaudio

from audio_utils import *

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
    # spectrogram = torchaudio.transforms.AmplitudeToDB()(spectrogram)
    return (spectrogram)
 
  # def spectro_gram():
  #   spectrogram = torchaudio.transforms.MFCC(
  #   sample_rate=SAMPLE_RATE,
  #   n_mfcc=24,
  #   melkwargs={'n_fft': NFFT,
  #             'hop_length': HOP_LEN,
  #             'win_length': WIN_LEN,
  #             'n_mels': N_MELS,
  #             'window_fn': WIN_FN}
  #   )
  #   return spectrogram

  @staticmethod
  def spectro_augment(spec, max_mask_pct=0.1, n_freq_masks=1, n_time_masks=1):
    _, n_mels, n_steps = spec.shape
    mask_value = spec.mean()
    aug_spec = spec

    freq_mask_param = max_mask_pct * n_mels
    for _ in range(n_freq_masks):
        aug_spec = transforms.FrequencyMasking(freq_mask_param)(aug_spec, mask_value)

    time_mask_param = max_mask_pct * n_steps
    for _ in range(n_time_masks):
        aug_spec = transforms.TimeMasking(time_mask_param)(aug_spec, mask_value)

    return aug_spec