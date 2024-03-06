from flask import Flask
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

config = {
    "debug": True,
    "port": 5000,
    "host": "0.0.0.0",
    "SECRET_KEY": "GUARD",
    "ACCESS_EXPIRE": 3600,
    "REFRESH_EXPIRE": 2592000
}


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./database.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)
socketio = SocketIO(app, engineio_logger=True, logger=True, broadcast=True)


@socketio.event
def connect():
    send("Connected")

@socketio.on('connect', namespace='/test_i')
def test_i_namespace_connect():
    pass

@socketio.on('connect', namespace='/test_a')
def test_a_namespace_connect():
    pass

# @socketio.on("a", namespace='/api/device/image_prediction')
# def image_prediction(prediction):
#     print("Predict")
