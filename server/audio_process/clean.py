import os
import numpy as np
from tqdm import tqdm
import torchaudio
import torch

from audio_utils import CLEAN, DELTA_TIME, RAW, SAMPLE_RATE, THRESHOLD


def envelope(y, rate, threshold):
    mask = []
    window_size = int(rate / 20)
    y_abs = torch.abs(y)
    y_abs = torch.nn.functional.pad(y_abs, (0, window_size-1))
    y_mean = y_abs.unfold(0, window_size, 1).max(1).values
    mask = y_mean > threshold
    return mask


def downsample_mono(path, sr):
    waveform, sample_rate = torchaudio.load(path)
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)
    if sample_rate != sr:
        resampler = torchaudio.transforms.Resample(
            orig_freq=sample_rate, new_freq=sr)
        waveform = resampler(waveform)
    return sr, waveform


def save_sample(sample, rate, target_dir, fn, ix):
    ext = fn.split('.')[-1]
    fn = '.'.join(fn.split('.')[:-1])
    fullname = f"{fn}_{str(ix)}.{ext}"
    dst_path = os.path.join(target_dir, fullname)
    if os.path.exists(dst_path):
        return
    torchaudio.save(dst_path, sample, rate, format="wav")


def split_wavs():
    if os.path.exists(CLEAN) is False:
        os.mkdir(CLEAN)
    classes = os.listdir(RAW)
    for _cls in classes:
        target_dir = os.path.join(CLEAN, _cls)
        if os.path.exists(target_dir) is False:
            os.mkdir(target_dir)
        else:
            continue
        src_dir = os.path.join(RAW, _cls)
        for fn in tqdm(os.listdir(src_dir)):
            src_fn = os.path.join(src_dir, fn)
            rate, wav = downsample_mono(src_fn, SAMPLE_RATE)
            delta_sample = int(DELTA_TIME*rate)
            mask = envelope(wav[0], rate, THRESHOLD)
            wav = wav[:, mask]
            # cleaned audio is less than a single sample
            # pad with zeros to delta_sample size
            length_signal = wav.shape[1]
            if length_signal < delta_sample:
                num_missing_samples = delta_sample - length_signal
                last_dim_padding = (0, num_missing_samples)
                sample = torch.nn.functional.pad(wav, last_dim_padding)
                save_sample(sample, rate, target_dir, fn, 0)
            # step through audio and save every delta_sample
            # discard the ending audio if it is too short
            else:
                trunc = wav.shape[1] % delta_sample
                for cnt, i in enumerate(np.arange(0, wav.shape[1]-trunc, delta_sample)):
                    start = int(i)
                    stop = int(i + delta_sample)
                    sample = wav[:, start:stop]
                    save_sample(sample, rate, target_dir, fn, cnt)


if __name__ == '__main__':
    split_wavs()
