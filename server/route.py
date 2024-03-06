from view.user_api import testuser
from view.index import index
from view.device_api import audio_input, image_input, image_stream
from view.auth_api import login, register, request_access_token

route = {
    "/": {
        "endpoint": "index",
        "view": index,
        "methods": ["GET"]
    },
    "/api/user/register": {
        "endpoint": "api user register",
        "view": register,
        "methods": ["POST"]
    },
    "/api/user/login": {
        "endpoint": "api user login",
        "view": login,
        "methods": ["POST"]
    },
    "/api/user/refresh-access": {
        "endpoint": "api user refresh token",
        "view": request_access_token,
        "methods": ["GET"]
    },
    "/api/user/device": {
        "endpoint": "api user add device",
        "view": None,
        "methods": ["POST"]
    },
    "/api/user/device": {
        "endpoint": "api user delete device",
        "view": None,
        "methods": ["DELETE"]
    },
    "/api/device/image_input": {
        "endpoint": "api receive image from device",
        "view": image_input,
        "methods": ["POST"]
    },
    "/api/device/<code>/image_stream": {
        "endpoint": "api image stream",
        "view": image_stream,
        "methods": ["GET"]
    },
    "/api/device/audio_input": {
        "endpoint": "api receive audio from device",
        "view": audio_input,
        "methods": ["POST"]
    }
}
