import torch


RAW = 'raw'
CLEAN = 'clean'
SAMPLE_RATE = 16000
DELTA_TIME = 5
CLASS_MAPPING = [
    "Cry",
    "Laugh",
    "Silence",
    "Talk"
]
THRESHOLD = 0
NUM_CLASSES = len(CLASS_MAPPING)
BATCH_SIZE = 64
EPOCHS = 101
LEARNING_RATE = 0.000002
N_MELS = 64
NFFT = 2048
N_MFCC = 24
HOP_LEN = int(10*(10**-3)*SAMPLE_RATE)
WIN_LEN = int(30*(10**-3)*SAMPLE_RATE)
WIN_FN = torch.hamming_window
