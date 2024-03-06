import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from model import YoloV1
from data import BabyDataset
from utils import (
    non_max_suppression,
    mean_average_precision,
    intersection_over_union,
    cellboxes_to_boxes,
    get_bboxes,
    get_bboxes_audio,
    plot_image,
    save_checkpoint,
    load_checkpoint,
)
from config import config

LEARNING_RATE = 2e-5
DEVICE = "cuda" if torch.cuda.is_available else "cpu"
# DEVICE = "cpu"
BATCH_SIZE = 16  # 64 in original paper but I don't have that much vram, grad accum?
WEIGHT_DECAY = 0
EPOCHS = 100
NUM_WORKERS = 2
PIN_MEMORY = True
LOAD_MODEL = False
LOAD_MODEL_FILE = "model"
START_EPOCH = 60

model = YoloV1(split_size=config["stride"], num_boxes=config["box_num"],
                   num_classes=config["class_num"]).to(DEVICE)
optimizer = optim.Adam(
        model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY
    )
load_checkpoint(torch.load(
            f"{LOAD_MODEL_FILE}.pth.tar"), model, optimizer)