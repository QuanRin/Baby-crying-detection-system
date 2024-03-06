import os
import cv2
import numpy as np
import yolov3_config as config
from yolov3_model import YOLOv3
from yolo3_utils import cells_to_bboxes, get_evaluation_bboxes, mean_average_precision, non_max_suppression, plot_image
import torch
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2
from yolov3_dataset import BabyDataset
from torch.utils.data import DataLoader

def main():
    model = YOLOv3(num_classes=config.CLASS_NUM).to(config.DEVICE)
    checkpoint = torch.load(os.path.join(os.path.dirname(
            __file__), 'checkpoint.pth.tar'),
                            map_location=config.DEVICE)
    model.load_state_dict(checkpoint["state_dict"])

    transforms = A.Compose(
        [
            A.LongestMaxSize(max_size=config.IMAGE_SIZE),
            A.PadIfNeeded(
                min_height=config.IMAGE_SIZE, min_width=config.IMAGE_SIZE, border_mode=cv2.BORDER_CONSTANT
            ),
            A.Normalize(mean=[0, 0, 0], std=[1, 1, 1], max_pixel_value=255,),
            ToTensorV2(),
        ],
    )

    anchors = (
        torch.tensor(config.ANCHORS)
        * torch.tensor(config.STRIDE).unsqueeze(1).unsqueeze(1).repeat(1, 3, 2)
    ).to(config.DEVICE)

    test_dataset = BabyDataset(
            transform=config.test_transforms, data_csv=config.IMAGE_TEST_CSV)
    test_loader = DataLoader(
            dataset=test_dataset,
            batch_size=config.BATCH_SIZE,
            num_workers=config.NUM_WORKERS,
            pin_memory=config.PIN_MEMORY,
            shuffle=True,
            drop_last=True,
        )

    tpred_boxes, ttrue_boxes = get_evaluation_bboxes(
                test_loader,
                model,
                iou_threshold=config.NMS_IOU_THRESH,
                anchors=config.ANCHORS,
                threshold=config.CONF_THRESHOLD,
            )
    tmapval = mean_average_precision(
        tpred_boxes,
        ttrue_boxes,
        iou_threshold=config.MAP_IOU_THRESH,
        box_format="midpoint",
        num_classes=config.CLASS_NUM,
    )

    print(f"Test | Precision: {tmapval[0]}, Recall: {tmapval[1]}, mAP: {tmapval[2]}")
if __name__ == '__main__':
    main()