"""
Main file for training Yolo model on Pascal VOC dataset

"""

import torch
import torchvision.transforms as transforms
import torch.optim as optim
import torchvision.transforms.functional as FT
from tqdm import tqdm
from torch.utils.data import DataLoader
from model import (YoloV1, TinyGuardian)
from data import (BabyDataset, TinyGuardianBabyDataset)
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
from loss import (YoloLoss, TinyGuardianLoss)
from config import config

import csv


seed = 123
torch.manual_seed(seed)

# Hyperparameters etc.
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


def train_fn(train_loader, model, optimizer, loss_fn):
    loop = tqdm(train_loader, leave=True)
    mean_loss = []

    for batch_idx, (x, y) in enumerate(loop):
        x, y = x.to(DEVICE), y.to(DEVICE)
        out = model(x)
        loss = loss_fn(out, y)
        mean_loss.append(loss.item())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # update progress bar
        loop.set_postfix(loss=loss.item())

    print(f"Mean loss was {sum(mean_loss)/len(mean_loss)}")
    return sum(mean_loss)/len(mean_loss)


def main():
    print("Loading model")
    model = YoloV1(split_size=config["stride"], num_boxes=config["box_num"],
                   num_classes=config["class_num"]).to(DEVICE)
    optimizer = optim.Adam(
        model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY
    )
    loss_fn = YoloLoss()

    if LOAD_MODEL:
        load_checkpoint(torch.load(
            f"{LOAD_MODEL_FILE}.pth.tar"), model, optimizer)

    print("Loading dataset")
    train_dataset = BabyDataset()

    # test_dataset = VOCDataset(
    #     "data/test.csv", transform=transform, img_dir=IMG_DIR, label_dir=LABEL_DIR,
    # )

    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        pin_memory=PIN_MEMORY,
        shuffle=True,
        drop_last=True,
    )

    # test_loader = DataLoader(
    #     dataset=test_dataset,
    #     batch_size=BATCH_SIZE,
    #     num_workers=NUM_WORKERS,
    #     pin_memory=PIN_MEMORY,
    #     shuffle=True,
    #     drop_last=True,
    # )

    losses = []
    mAPs = []

    for epoch in range(EPOCHS):
        print(f"Epoch: {epoch + 1}")
        # for x, y in train_loader:
        #     x = x.to(DEVICE)
        #     for idx in range(8):
        #         bboxes = cellboxes_to_boxes(model(x))
        #         bboxes = non_max_suppression(
        #             bboxes[idx], iou_threshold=0.5, threshold=0.4, box_format="midpoint")
        #         plot_image(x[idx].permute(1, 2, 0).to("cpu"), bboxes)

        #    import sys
        #    sys.exit()
        loss = train_fn(train_loader, model, optimizer, loss_fn)
        losses.append(loss)

        if epoch % 10 == 0:
            pred_boxes, target_boxes = get_bboxes(
                train_loader, model, iou_threshold=0.5, threshold=0.4, device=DEVICE
            )

            mean_avg_prec_1 = mean_average_precision(
                pred_boxes, target_boxes, iou_threshold=0.5, box_format="midpoint"
            )
            print(f"Train mAP@0.75: {mean_avg_prec_1}")
            mAPs.append(mean_avg_prec_1.item())
        else:
            mAPs.append(mAPs[-1])

        if epoch % 100 == 0:
            #    import time
            #    time.sleep(10)

            print("Saving checkpoint")
            checkpoint = {
                "state_dict": model.state_dict(),
                "optimizer": optimizer.state_dict(),
            }
            save_checkpoint(
                checkpoint, filename=f"{LOAD_MODEL_FILE}.{epoch}.pth.tar")

    print(losses, mAPs)
    with open('loss.csv', 'w') as f:
        writer = csv.writer(f)
        for loss, mAP in zip(losses, mAPs):
            writer.writerow([loss, str(mAP)])

# def train_fn(train_loader, model, optimizer, loss_fn):
#     loop = tqdm(train_loader, leave=True)
#     mean_loss = []

#     for batch_idx, (x_img, x_aud, y_img, y_aud) in enumerate(loop):
#         x_img, x_aud, y_img, y_aud = x_img.to(DEVICE), x_aud.to(
#             DEVICE), y_img.to(DEVICE), y_aud.to(DEVICE)
#         out = model(x_img, x_aud)
#         loss = loss_fn(out, y_img, y_aud)
#         mean_loss.append(loss.item())
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()

#         # update progress bar
#         loop.set_postfix(loss=loss.item())

#     print(f"Mean loss was {sum(mean_loss)/len(mean_loss)}")
#     return sum(mean_loss)/len(mean_loss)


# def main():
#     print('Loading TinyGuardian model')
#     model = TinyGuardian(
#         split_size=config["stride"], num_boxes=config["box_num"], num_classes=config["class_num"], aud_out_extra=config['aud_class_num']).to(DEVICE)
#     optimizer = optim.Adam(
#         model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY
#     )
#     loss_fn = TinyGuardianLoss()

#     if LOAD_MODEL:
#         load_checkpoint(torch.load(
#             f"{LOAD_MODEL_FILE}.pth.tar"), model, optimizer)
#     print("Loading dataset")
#     train_dataset = TinyGuardianBabyDataset()
#     train_loader = DataLoader(
#         dataset=train_dataset,
#         batch_size=BATCH_SIZE,
#         num_workers=NUM_WORKERS,
#         pin_memory=PIN_MEMORY,
#         shuffle=True,
#         drop_last=True,
#     )
#     losses = []
#     mAPs = []

#     for epoch in range(START_EPOCH + 1, EPOCHS + 1, 1):
#         print(f"Epoch: {epoch}")
#         # for x, y in train_loader:
#         #     x = x.to(DEVICE)
#         #     for idx in range(8):
#         #         bboxes = cellboxes_to_boxes(model(x))
#         #         bboxes = non_max_suppression(
#         #             bboxes[idx], iou_threshold=0.5, threshold=0.4, box_format="midpoint")
#         #         plot_image(x[idx].permute(1, 2, 0).to("cpu"), bboxes)

#         #    import sys
#         #    sys.exit()
#         loss = train_fn(train_loader, model, optimizer, loss_fn)
#         losses.append(loss)

#         if epoch % 1 == 0:
#             pred_boxes, target_boxes = get_bboxes_audio(
#                 train_loader, model, iou_threshold=0.5, threshold=0.4, device=DEVICE
#             )

#             mean_avg_prec_1 = mean_average_precision(
#                 pred_boxes, target_boxes, iou_threshold=0.5, box_format="midpoint"
#             )
#             print(f"Train mAP@0.75: {mean_avg_prec_1}")
#             mAPs.append(mean_avg_prec_1.item())
#         else:
#             mAPs.append(mAPs[-1])

#         if epoch % 10 == 0:
#             #    import time
#             #    time.sleep(10)

#             print("Saving checkpoint")
#             checkpoint = {
#                 "state_dict": model.state_dict(),
#                 "optimizer": optimizer.state_dict(),
#             }
#             save_checkpoint(
#                 checkpoint, filename=f"{LOAD_MODEL_FILE}.{epoch}.pth.tar")

#     print(losses, mAPs)
#     with open('loss.csv', 'w') as f:
#         writer = csv.writer(f)
#         for loss, mAP in zip(losses, mAPs):
#             writer.writerow([loss, str(mAP)])


if __name__ == "__main__":
    main()
