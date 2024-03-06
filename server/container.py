from repository.test_repository import TestRepository
from service.device_service import DeviceService
from service.user_service import UserService
from service.auth_service import AuthService
from service.baby_service import BabyService
from enum import Enum

import config

db = config.db


class Component(str, Enum):
    App = "App"
    Db = "Db",
    DeviceService = "DeviceService",
    BabyService = "BabyService",
    UserService = "UserService",
    TestRepository = "TestRepository",
    AuthenticationService = "AuthenticationService"


_userService = UserService(db=db)

container = {
    Component.DeviceService: DeviceService(),
    Component.BabyService: BabyService(),
    Component.UserService: _userService,
    Component.TestRepository: TestRepository(),
    Component.AuthenticationService: AuthService()
}


class Event(str, Enum):
    ImagePrediction = "ImagePrediction"
    AudioPrediction = "AudioPrediction"
