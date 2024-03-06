from PIL import Image
# from baby_recognizer import yolov3_prediction as yolo
from model.predict_model import (
    ImagePredict, 
    AudioPredict, 
    BoundingBox
    )
from baby_recognizer import yolov3_prediction as yolo


class DeviceService:
    def __init__(self) -> None:
        pass

    def predict_image(self, image) -> ImagePredict:
        image = Image.open(image)
        bboxes = yolo.predict(image)
        bboxes = list(map(lambda e: BoundingBox(
            x=e[2],
            y=e[3],
            w=e[4],
            h=e[5],
            label=e[0],
            confidence=e[1]
        ), bboxes))
        return ImagePredict(bboxes=bboxes)

    # def predict_image(self, image) -> ImagePredict:
    #     return ImagePredict(bboxes=[
    #         BoundingBox(0.2, 0.3, 0.3, 0.2, 0, 1)
    #     ])

    def predict_audio(audio) -> AudioPredict:
        # return AudioPredict(wavform=torch_wav, sample_rate=torch_sample)
        pass
