from http import HTTPStatus
import json
import cv2
from flask import jsonify, request, Response
from flask_socketio import emit, send
from config import socketio
from container import container, Component, Event
from model.predict_model import ImagePredict, AudioPredict, Prediction
from service.device_service import DeviceService
from service.models import WrapResponseDto
import torchaudio
from io import BytesIO

data = b''
last_image_prediction = None
last_audio_prediction = None

def image_input():
    image = request.files.get('imageFile')
    if not image:
        return Response(
            headers={
                "Content-Type": "application/json"
            },
            response=json.dumps(WrapResponseDto.error(
                "Bad request", "imageFile is missing").to_json()),
            status=HTTPStatus.BAD_REQUEST
        )
        
    global data
    data = image.read()

    device_service: DeviceService = container.get(Component.DeviceService)
    prediction: ImagePredict = device_service.predict_image(image)
    global last_image_prediction
    last_image_prediction = prediction
    prediction = Prediction(last_image_prediction, last_audio_prediction)
    emit(Event.ImagePrediction, prediction.to_json(),
         namespace="/test_i", broadcast=True)
    return Response(
        headers={
            "Content-Type": "application/json"
        },
        response=json.dumps(WrapResponseDto.success(
            prediction.to_json(), "Successfully").to_json()),
        status=HTTPStatus.OK
    )

def image_feed(code):
    while True:
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')

def image_stream(code):
    return Response(image_feed(code), mimetype='multipart/x-mixed-replace; boundary=frame')


def audio_input():
    audio = request.files.get('audioFile')
    audio = BytesIO(audio.read())
    audio, sr = torchaudio.load(audio)
    prediction = AudioPredict(wavform=audio)
    global last_audio_prediction
    last_audio_prediction = prediction
    prediction = Prediction(last_image_prediction, last_audio_prediction)
    emit(Event.AudioPrediction, prediction.to_json(), namespace="/test_a", broadcast=True)
    return Response(
        headers={
            "Content-Type": "application/json"
        },
        response=json.dumps(WrapResponseDto.success(prediction.to_json(), "Sucessfully").to_json()),
        status=HTTPStatus.OK
    )
