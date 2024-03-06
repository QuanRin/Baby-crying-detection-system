from http import HTTPStatus
from flask import request, Response
from container import container, Component
from service.user_service import UserService


def testuser():
    userService: UserService = container[Component.UserService]
    username = request.json['username']
    age = request.json['age']
    email = request.json['email']
    userService.create(username=username, age=age, email=email)
    return Response(status=HTTPStatus.OK, response="Created")
