from http import HTTPStatus
from flask import Response, request
from service.auth_service import AuthService
from service.models import LoginRequestDto, RegisterRequestDto, WrapResponseDto
from util.security import token_required
import json


# @api.route("/login", methods=["POST"])
def login():
    try:
        token = request.headers.get("Authorization")
        data = request.json
        login_request = LoginRequestDto.from_json(data)
        
        response = AuthService.login(login_request)
        print(response.to_json())
        if response.is_error:
            return Response(
                response=json.dumps(response.to_json()),
                status=HTTPStatus.BAD_REQUEST,
                headers={
                    "Content-Type": "application/json"
                }
            )
        return Response(
            response=json.dumps(response.to_json()),
            status=HTTPStatus.BAD_REQUEST if response.error == "Unauthorized" else HTTPStatus.BAD_REQUEST if response.is_error else HTTPStatus.OK,
            headers={
                "Content-Type": "application/json"
            }
        )
    except Exception as e:
        raise e
        return Response(
            response=json.dumps(WrapResponseDto.error(str(e)).to_json()),
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            headers={
                "Content-Type": "application/json"
            }
        )


# @api.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        register_request = RegisterRequestDto.from_json(data)
        response = AuthService.register(register_request)
        return Response(
            response=json.dumps(response.to_json()),
            status=HTTPStatus.BAD_REQUEST if response.is_error else HTTPStatus.OK,
            headers={
                "Content-Type": "application/json"
            }
        )
    except Exception as e:
        return Response(
            response=json.dumps(WrapResponseDto.error(str(e)).to_json()),
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            headers={
                "Content-Type": "application/json"
            }
        )


# @api.route("/logout", methods=["POST"])
@token_required
def logout(user):
    try:
        token = request.headers["Authorization"]
        response = AuthService.logout(token)
        return Response(
            response=json.dumps(response.to_json()),
            status=HTTPStatus.OK,
            headers={
                "Content-Type": "application/json"
            }
        )
    except Exception as e:
        return Response(
            response=json.dumps(WrapResponseDto.error(str(e)).to_json()),
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            headers={
                "Content-Type": "application/json"
            }
        )


# @api.route("/refresh-access", methods=["GET"])
def request_access_token():
    try:
        token = request.args.get("refresh-token")
        response = AuthService.request_access_token(token)
        return Response(
            response=json.dumps(response.to_json()),
            status=HTTPStatus.OK,
            headers={
                "Content-Type": "application/json"
            }
        )
    except Exception as e:
        return Response(
            response=json.dumps(WrapResponseDto.error(str(e)).to_json()),
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            headers={
                "Content-Type": "application/json"
            }
        )
