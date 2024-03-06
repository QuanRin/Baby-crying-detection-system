import os
import csv
import glob
from pathlib import Path
import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset
from . import yolov3_config as config
# import yolov3_config as config
import albumentations as A
from .yolo3_utils import (
    iou_width_height as iou
)
# from yolo3_utils import (
#     iou_width_height as iou
# )


class BabyDataset(Dataset):
    def __init__(self, config=config, data_csv=config.IMAGE_DATA_CSV, transform: A.Compose = None):
        self.S = config.STRIDE
        self.C = config.CLASS_NUM
        self.anchors = config.ANCHORS
        self.anchors = torch.tensor(
            self.anchors[0] + self.anchors[1] + self.anchors[2])

        self.ignore_iou_thresh = 0.5
        self.transform = transform

        self._image_data = []

        with open(data_csv) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                self._image_data.append(row)

    def __len__(self):
        return len(self._image_data)

    def __getitem__(self, index):
        img_path, label_pth = self._image_data[index]
        boxes = []
        with open(label_pth, "r") as f:
            for label in f.readlines():
                class_label, xc, yc, w, h = label.replace("\n", "").split()
                class_label = int(class_label)
                xc, yc, w, h = map(float, [xc, yc, w, h])
                boxes.append(np.array([class_label, xc, yc, w, h]))

        image = np.array(Image.open(img_path).convert("RGB"))
        if len(boxes) > 0:
            boxes = np.roll(boxes, 4, axis=1)

        if self.transform:
            augmentations = self.transform(image=image, bboxes=boxes)
            image = augmentations["image"]
            boxes = augmentations["bboxes"]

        labels = [torch.zeros(3, S, S, 6) for S in self.S]
        for box in boxes:
            iou_anchors = iou(torch.tensor(
                box[2:4]).unsqueeze(0), self.anchors)

            anchor_indices = iou_anchors.argsort(descending=True, dim=0)
            x, y, w, h, class_label = box
            has_anchor = [False for _ in range(3)]

            for anchor_index in anchor_indices:
                s_index = anchor_index // 3
                a_index = anchor_index % 3
                S = self.S[s_index]
                i, j = int(S * y), int(S * x)
                a_taken = labels[s_index][a_index, i, j, 0]
                if not a_taken and not has_anchor[s_index]:
                    labels[s_index][a_index, i, j, 0] = 1
                    x_cell, y_cell = S * x - j, S * y - i
                    w_cell, h_cell = w * S, h * S
                    box_coord = torch.tensor([x_cell, y_cell, w_cell, h_cell])
                    labels[s_index][a_index, i, j, 1:5] = box_coord
                    labels[s_index][a_index, i, j, 5] = int(class_label)
                    has_anchor[s_index] = True
                elif not a_taken and iou_anchors[a_index] > self.ignore_iou_thresh:
                    labels[s_index][a_index, i, j, 0] = -1  # ignore prediction
        return image, tuple(labels)


def analyze(data):
    cry = 0
    nocry = 0
    obj = 0
    noobj = 0
    for p in data:
        label_path = p[1]
        if os.stat(label_path).st_size == 0:
            noobj += 1
            continue
        obj += 1
        with open(label_path) as f:
            for line in f:
                adata = line.split()
                if adata[0] == '0':
                    cry += 1
                elif adata[0] == '1':
                    nocry += 1
    osum = noobj + obj
    csum = nocry + cry
    print(f'Total: {len(data)}')
    print(f'No object: {noobj * 100 / osum}%')
    print(f'Object: {obj * 100 / osum}%')
    print(f'\t- Cry: {cry * 100 / csum}%')
    print(f'\t- No Cry: {nocry * 100 / csum}%')


def preprocess_csv(config=config, split=(0.6, 0.2, 0.2)):
    data = []
    for path in glob.glob(config.IMAGE_DATA_PATH + "**/**.jpg", recursive=True):
        _path = Path(path)
        if _path.suffix == '.txt':
            continue

        parent = _path.parent
        name = _path.stem
        if not Path.joinpath(parent, name + ".txt").exists():
            open(Path.joinpath(parent, name + ".txt"), 'x')

        data.append(
            [str(_path), str(Path.joinpath(parent, name + ".txt"))])
    for path in glob.glob(config.IMAGE_DATA_PATH + "**/**.png", recursive=True):
        _path = Path(path)
        if _path.suffix == '.txt':
            continue

        parent = _path.parent
        name = _path.stem
        if not Path.joinpath(parent, name + ".txt").exists():
            open(Path.joinpath(parent, name + ".txt"), 'x')

        data.append(
            [str(_path), str(Path.joinpath(parent, name + ".txt"))])

    import random
    random.shuffle(data)
    train_l = int(len(data) * split[0])
    val_l = int(len(data) * split[1])
    test_l = int(len(data) * split[2])

    # split_l = int(len(data) * split)
    train_data = data[:train_l]
    data = data[train_l:]
    val_data = data[:val_l]
    data = data[val_l:]
    test_data = data

    print('Train data:')
    analyze(train_data)
    print('Validate data:')
    analyze(val_data)
    print('Test data:')
    analyze(test_data)

    with open(config.IMAGE_DATA_CSV, 'w') as f:
        writer = csv.writer(f, lineterminator='\r')
        for data in train_data:
            writer.writerow(data)
    with open(config.IMAGE_TEST_CSV, 'w') as f:
        writer = csv.writer(f, lineterminator='\r')
        for data in test_data:
            writer.writerow(data)
    with open(config.IMAGE_VAL_CSV, 'w') as f:
        writer = csv.writer(f, lineterminator='\r')
        for data in val_data:
            writer.writerow(data)


if __name__ == '__main__':
    preprocess_csv()
    # baby = BabyDataset()
