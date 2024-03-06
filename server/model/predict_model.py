import torchaudio
import torch
import json
from entity.device import Device
from baby_audio import predict_one, DELTA_TIME, SAMPLE_RATE


class BoundingBox:
    def __init__(self, x, y, w, h, label, confidence) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = int(label)
        self.confidence = confidence

    def to_json(self, to_string: bool = False) -> dict[str, any] | str:
        json_obj = dict(x=self.x, y=self.y, w=self.w, h=self.h,
                        label=self.label, confidence=self.confidence)
        if to_string:
            return json.dumps(json_obj)
        return json_obj


class ImagePredict:
    def __init__(self, bboxes: list[BoundingBox], device: Device = None) -> None:
        self.bboxes = bboxes
        self.device = device
        is_crying = False
        for bbox in bboxes:
            is_crying = is_crying or bbox.label == 0
        self.is_crying = is_crying

    def to_json(self, to_string: bool = False) -> dict[str, any] | str:
        json_obj = dict(
            device=self.device.to_json() if self.device else Device(code="test").to_json(),
            bboxes=list(map(lambda e: e.to_json(),
                        self.bboxes)),
            is_crying=self.is_crying)
        if to_string:
            return json.dumps(json_obj)
        return json_obj


THRESHOLD = 0.15


def envelope(y, rate, threshold):
    mask = []
    window_size = int(rate / 20)
    y_abs = torch.abs(y)
    y_abs = torch.nn.functional.pad(y_abs, (0, window_size-1))
    y_mean = y_abs.unfold(0, window_size, 1).max(1).values
    mask = y_mean > threshold
    return mask


# def downsample_mono(waveform, sample_rate, sr):
#     if waveform.shape[0] > 1:
#         waveform = torch.mean(waveform, dim=0, keepdim=True)
#     if sample_rate != sr:
#         resampler = torchaudio.transforms.Resample(
#             orig_freq=sample_rate, new_freq=sr)
#         waveform = resampler(waveform)
#     return sr, waveform


def truncate(wavform):
    delta_sample = int(DELTA_TIME*SAMPLE_RATE)
    mask = envelope(wavform.reshape(-1), SAMPLE_RATE, THRESHOLD)
    wav = wavform[:, mask]
    length_signal = wav.shape[1]
    if length_signal < delta_sample:
        wav = torch.nn.functional.pad(
            wav, (0, delta_sample-length_signal))
        return wav
    else:
        return wav[:, :DELTA_TIME*SAMPLE_RATE]


class AudioPredict:
    def __init__(self, wavform) -> None:
        self.wav = truncate(wavform=wavform)
        self.prediction = None
        self.score = None
        self.prediction, self.score = predict_one(waveform=self.wav)
        self.is_crying = self.prediction == "Cry"

    def to_json(self, to_string: bool = False) -> dict[str, any] | str:
        json_obj = dict(prediction=self.prediction, score=self.score, is_crying=self.is_crying)
        if to_string:
            return json.dumps(json_obj)
        return json_obj

class Prediction:
    def __init__(self, image_prediction: ImagePredict = None, audio_prediction: AudioPredict = None) -> None:
        self.audio_prediction = audio_prediction
        self.image_prediction = image_prediction
    
    def to_json(self, to_string: bool = False) -> dict[str, any] | str:
        json_obj = dict(
            audio_prediction=self.audio_prediction.to_json(to_string) if self.audio_prediction != None else None,
            image_prediction=self.image_prediction.to_json(to_string) if self.image_prediction != None else None,
        )
        if self.image_prediction and self.audio_prediction:
            json_obj["is_crying"] = self.audio_prediction.is_crying and self.image_prediction.is_crying
            
        if to_string:
            return json.dumps(json_obj)
        return json_obj