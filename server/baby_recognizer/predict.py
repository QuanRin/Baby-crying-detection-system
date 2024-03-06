import cv2
from model import TinyGuardian, YoloV1
import torch.optim as optim
from loss import YoloLoss
from config import config
from utils import (
    non_max_suppression,
    mean_average_precision,
    intersection_over_union,
    cellboxes_to_boxes,
    get_bboxes,
    plot_image,
    save_checkpoint,
    load_checkpoint,
)
import torch
from PIL import Image
import torchvision.transforms as transforms
import torchaudio

# Hyperparameters etc.
LEARNING_RATE = 2e-5
# DEVICE = "cuda" if torch.cuda.is_available else "cpu"
DEVICE = "cuda"
BATCH_SIZE = 8  # 64 in original paper but I don't have that much vram, grad accum?
WEIGHT_DECAY = 0
EPOCHS = 1000
NUM_WORKERS = 2
PIN_MEMORY = True
LOAD_MODEL = True
LOAD_MODEL_FILE = "model.20.30.pth.tar"

model = TinyGuardian(split_size=config["stride"], num_boxes=config["box_num"],
                     num_classes=config["class_num"], aud_out_extra=config['aud_class_num']).to(DEVICE)
optimizer = optim.Adam(
    model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY
)
# loss_fn = YoloLoss()

if LOAD_MODEL:
    load_checkpoint(torch.load(LOAD_MODEL_FILE), model, optimizer)

transform = transforms.Compose(
    [transforms.Resize((448, 448)), transforms.ToTensor()])
x_img = Image.open('./dataset/test/1.jpg').convert("RGB")
x_img = transform(x_img)
x_aud, rate = torchaudio.load('./dataset/clean/Cry/101e7_3.wav')
x_aud = torchaudio.transforms.MelSpectrogram(
    sample_rate=rate/2, n_fft=251)(x_aud)

y = model(x_img.unsqueeze(0).to(DEVICE), x_aud.unsqueeze(0).to(DEVICE))

y = y[..., :-config['aud_class_num']]

bboxes = cellboxes_to_boxes(y)
print(bboxes)
bbboxes = non_max_suppression(
    bboxes[0], iou_threshold=0.5, threshold=0.4, box_format="midpoint")
plot_image(x_img.permute(1, 2, 0).to("cpu"), bbboxes)

frame_step = 1


def draw_box(image, bboxs):
    width, height, _ = image.shape
    for box in bboxs:
        pred_class = "Crying" if box[0] < 1 else "Not Crying"
        box = box[2:]
        assert len(box) == 4, "Got more values than in x, y, w, h, in a box!"
        x = int((box[0] - box[2] / 2) * width)
        y = int((box[1] - box[3] / 2) * height)
        w = int(width * box[2])
        h = int(height * box[3])
        image = cv2.rectangle(
            image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        image = cv2.putText(image, pred_class, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    return image


def plot_video():
    image_counter = 0
    read_counter = 0
    src = cv2.VideoCapture('./dataset/test/video.mp4')
    while src.isOpened():
        ret, img = src.read()
        if ret and read_counter % frame_step == 0:
            converted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(converted)
            x = transform(pil_im)
            y = model(x.unsqueeze(0).to(DEVICE), x_aud.unsqueeze(0).to(DEVICE))
            y = y[..., :-config['aud_class_num']]
            print(y[..., -config['aud_class_num']:])
            bboxes = cellboxes_to_boxes(y)
            bbboxes = non_max_suppression(
                bboxes[0], iou_threshold=0.5, threshold=0.4, box_format="midpoint")
            image = draw_box(img, bbboxes)
            cv2.imshow('Frame', image)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            image_counter += 1
        elif not ret:
            break
        read_counter += 1
    src.release()


plot_video()
