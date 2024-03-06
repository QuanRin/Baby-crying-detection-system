import os
import cv2
import numpy as np
from .yolo3_utils import cells_to_bboxes, non_max_suppression, plot_image
from .yolov3_model import YOLOv3
from . import yolov3_config as config
# import yolov3_config as config
# from yolov3_model import YOLOv3
# from yolo3_utils import cells_to_bboxes, non_max_suppression, plot_image
import torch
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2

model = YOLOv3(num_classes=config.CLASS_NUM).to(config.DEVICE)
checkpoint = torch.load(os.path.join(os.path.dirname(
        __file__), 'checkpoint.pth.tar'),
                        map_location=config.DEVICE)
# checkpoint = torch.load('./model/checkpoint.pth.tar',
#                         map_location=config.DEVICE)
model.load_state_dict(checkpoint["state_dict"])

# image = np.array(Image.open(
#     './dataset/src/image23.jpg').convert('RGB'))
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
# image = transforms(image=image)['image']
anchors = (
    torch.tensor(config.ANCHORS)
    * torch.tensor(config.STRIDE).unsqueeze(1).unsqueeze(1).repeat(1, 3, 2)
).to(config.DEVICE)
# with torch.no_grad():
#     out = model(image.unsqueeze(0).to(config.DEVICE))
#     bboxes = [[] for _ in range(image.shape[0])]
#     for i in range(3):
#         batch_size, A, S, _, _ = out[i].shape
#         anchor = anchors[i]
#         boxes_scale_i = cells_to_bboxes(
#             out[i], anchor, S=S, is_preds=True
#         )
#         for idx, (box) in enumerate(boxes_scale_i):
#             bboxes[idx] += box
# nms_boxes = non_max_suppression(
#     bboxes[0], iou_threshold=0.5, threshold=0.8, box_format="midpoint",
# )
# print(nms_boxes)
# plot_image(image.permute(1, 2, 0).detach().cpu(), nms_boxes)


def draw_box(image, bboxs):
    width, height, _ = image.shape
    for box in bboxs:
        pred_class = "Crying" if box[0] < 1 else "Not Crying"
        box = box[2:]
        if box[2] > 10000 or box[3] > 10000:
            continue
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


frame_step = 1


def plot_video(nums_of_baby=1):
    image_counter = 0
    read_counter = 0
    src = cv2.VideoCapture('./dataset/test/video.mp4')
    while src.isOpened():
        ret, img = src.read()
        if ret and read_counter % frame_step == 0:
            converted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.imshow('Before', img)
            x = transforms(image=converted)[
                'image'].unsqueeze(0).to(config.DEVICE)
            y = model(x)
            trans_img = x[0].permute(1, 2, 0).cpu().numpy()
            print(trans_img.shape)
            trans_img = cv2.cvtColor(trans_img, cv2.COLOR_RGB2BGR)
            bboxes = [[] for _ in range(x.shape[0])]
            for i in range(3):
                batch_size, A, S, _, _ = y[i].shape
                anchor = anchors[i]
                boxes_scale_i = cells_to_bboxes(
                    y[i], anchor, S=S, is_preds=True
                )
                for idx, (box) in enumerate(boxes_scale_i):
                    bboxes[idx] += box
            nms_boxes = non_max_suppression(
                bboxes[0], iou_threshold=0.5, threshold=0.8, box_format="midpoint",
            )
            print(nms_boxes)
            image = draw_box(trans_img, nms_boxes[:nums_of_baby])
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

def reverse_transform(image, box):
    h = image.shape[0]
    w = image.shape[1]
    h_dif = max([h, w]) - h
    w_dif = max([h, w]) - w
    h_pad = (h_dif / 2) / max([h, w])
    w_pad = (w_dif / 2) / max([h, w])
    
    box[2] = (box[2] - w_pad) / (1 - 2 * w_pad)
    box[3] = (box[3] - h_pad) / (1 - 2 * h_pad)
    box[4] = box[4] / (1 - 2 * w_pad)
    box[5] = box[5] / (1 - 2 * h_pad)
    
    return box

def predict(image, do_reverse_transform=True):
    image = np.array(image.convert('RGB'))
    t_image = transforms(image=image)['image']
    anchors = (
        torch.tensor(config.ANCHORS)
        * torch.tensor(config.STRIDE).unsqueeze(1).unsqueeze(1).repeat(1, 3, 2)
    ).to(config.DEVICE)
    with torch.no_grad():
        out = model(t_image.unsqueeze(0).to(config.DEVICE))
        bboxes = [[] for _ in range(t_image.shape[0])]
        for i in range(3):
            batch_size, A, S, _, _ = out[i].shape
            anchor = anchors[i]
            boxes_scale_i = cells_to_bboxes(
                out[i], anchor, S=S, is_preds=True
            )
            for idx, (box) in enumerate(boxes_scale_i):
                bboxes[idx] += box
    nms_boxes = non_max_suppression(
        bboxes[0], iou_threshold=0.5, threshold=0.85, box_format="midpoint",
    )
    if do_reverse_transform:
        nms_boxes = map(lambda box: reverse_transform(image, box), nms_boxes)
    return nms_boxes
