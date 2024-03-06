from pydub import AudioSegment, playback
import os
import torchaudio
import torch

# for fn in os.listdir(os.path.join('clean', 'Cry')):
#     sound_file = AudioSegment.from_wav(
#         os.path.join('clean', 'Cry', fn))
#     sound_file = sound_file-10
#     sound_file.export(os.path.join('clean', 'Cry', fn), format='wav')
# playback.play(audio)
# waveform, sample_rate = torchaudio.load(
#     os.path.join('raw', 'Cat', 'catsound.wav'))
# adjusted_waveform = waveform*0.7
# torchaudio.save(os.path.join('raw', 'Cat', 'catsound.wav'),
#                 adjusted_waveform, sample_rate)
sound_file = AudioSegment.from_wav(
    os.path.join('raw', 'Cry', "cryyy.wav"))
sound_file = sound_file[8000:]
sound_file.export(os.path.join('raw', 'Cry', "cryyy.wav"), format='wav')
