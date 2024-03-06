from http import HTTPStatus
from flask import Response
from container import container, Component
from repository.test_repository import TestRepository
# from service.auth_service import AuthenticationService
from service.baby_service import BabyService

import json


def index():
    baby_service: BabyService = container[Component.BabyService]
    test_repo: TestRepository = container[Component.TestRepository]
    return f"<p>{test_repo.get()}, your baby is crying: {baby_service.is_crying()}<p>"