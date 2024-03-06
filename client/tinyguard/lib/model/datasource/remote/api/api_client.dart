import 'dart:io';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:tinyguard/model/datasource/remote/api/api_exception.dart';
import 'package:tinyguard/model/datasource/remote/entity/auth_entity.dart';
import 'package:tinyguard/model/shared/constants.dart';
import 'package:tinyguard/model/shared_preferences/spref_auth_model.dart';
import 'package:tinyguard/flavor_config.dart';
import 'package:tinyguard/utils/log_utils.dart';

class APIClient {
  final Dio dio = Dio();

  final SPrefAuthModel sPref;

  APIClient({required this.sPref}) {
    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (request, handler) {
          final String? accessToken = sPref.accessToken;
          if (accessToken != null && accessToken.isNotEmpty) {
            request.headers['Authorization'] = '$accessToken';
          }
          return handler.next(request);
        },
        onError: (error, handler) async {
          if (error.response?.statusCode == HttpStatus.unauthorized) {
            try {
              await handleRefreshToken();
              return handler.resolve(await _retry(error.requestOptions));
            } on DioException catch (e) {
              LogUtils.e(e.response?.data.toString() ?? "Unknown error");
              return handler.reject(error);
            }
          }
          return handler.reject(error);
        },
      ),
    );
  }

  Future<dynamic> get({required String url}) async {
    final String? accessToken = sPref.accessToken;
    Options options = Options();
    if (accessToken != null && accessToken.isNotEmpty) {
      options = Options(headers: {'Authorization': '$accessToken'});
    }
    try {
      String uri = '${FlavorConfig.instance.baseURL}$url';
      LogUtils.methodIn(message: uri);
      final response = await dio.get(uri, options: options);
      LogUtils.methodOut(message: '${response.data}');
      return response.data;
    } on DioException catch (dioError) {
      onError(dioError);
    }
  }

  Future<dynamic> post({
    required String url,
    dynamic data,
    Options? requestOptions,
  }) async {
    final String? accessToken = sPref.accessToken;
    // try {
    Options options = Options();
    if (requestOptions != null) {
      options = requestOptions;
    }
    if (accessToken != null && accessToken.isNotEmpty) {
      options.headers = {'Authorization': '$accessToken'};
    }
    String uri = '${FlavorConfig.instance.baseURL}$url';
    LogUtils.methodIn(message: uri);
    debugPrint(options.headers.toString());
    final response = await dio.post(uri, data: data, options: options);
    return response.data;
    // } on DioException catch (dioError) {
    //   onError(dioError);
    // }
  }

  Future<dynamic> put({
    required String url,
    dynamic data,
    Options? requestOptions,
  }) async {
    final String? accessToken = sPref.accessToken;
    try {
      Options options = Options();
      if (requestOptions != null) {
        options = requestOptions;
      }
      if (accessToken != null && accessToken.isNotEmpty) {
        options.headers = {'Authorization': '$accessToken'};
      }
      String uri = '${FlavorConfig.instance.baseURL}$url';
      LogUtils.methodIn(message: uri);
      final response = await dio.put(uri, data: data, options: options);
      return response.data;
    } on DioException catch (dioError) {
      onError(dioError);
    }
  }

  Future<dynamic> delete({
    required String url,
    Options? requestOptions,
  }) async {
    final String? accessToken = sPref.accessToken;
    try {
      Options options = Options();
      if (requestOptions != null) {
        options = requestOptions;
      }
      if (accessToken != null && accessToken.isNotEmpty) {
        options.headers = {'Authorization': '$accessToken'};
      }
      String uri = '${FlavorConfig.instance.baseURL}$url';
      LogUtils.methodIn(message: uri);
      final response = await dio.delete(uri, options: options);
      return response.data;
    } on DioException catch (dioError) {
      onError(dioError);
    }
  }

  void onError(DioException err) {
    (err.response == null)
        ? 'RESPONSE NULL !!!!'
        : debugPrint('ON ERROR: ' +
            err.response!.data.toString() +
            ' STATUS CODE: ' +
            err.response!.statusCode.toString());
    if (err.response != null) {
      switch (err.response?.statusCode) {
        case HttpStatus.badRequest:
          throw BadRequestException(
            message: err.response!.data['message'] as String?,
          );
        case HttpStatus.unauthorized:
          throw UnauthorizedException();
        case HttpStatus.forbidden:
          throw ForbiddenException();
        case HttpStatus.notFound:
          throw NotFoundException();
        case HttpStatus.conflict:
          throw ConflictException();
        case HttpStatus.internalServerError:
          throw InternalServerErrorException();
      }
    } else {
      switch (err.type) {
        case DioExceptionType.connectionTimeout:
        case DioExceptionType.sendTimeout:
        case DioExceptionType.receiveTimeout:
          throw DeadlineExceededException();
        case DioExceptionType.badResponse:
          throw BadRequestException();
        case DioExceptionType.cancel:
        case DioExceptionType.connectionError:
        case DioExceptionType.unknown:
          throw NoInternetConnectionException();
        case DioExceptionType.badCertificate:
          throw InternalServerErrorException();
      }
    }
  }
}

extension APIClientRefreshToken on APIClient {
  Future<void> handleRefreshToken() async {
    LogUtils.methodIn(message: 'refreshToken');
    try {
      final response = await get(
        url: 'user/refresh-access?refresh-token=${sPref.refreshToken}',
      );
      final authEntity = AuthEntity.fromJson(response as Map<String, dynamic>);
      await sPref.setAccessToken(
        value: authEntity.result?.accessToken ?? Constants.kEmptyString,
      );
      LogUtils.d("Set new access token: ${sPref.accessToken}");
    } catch (e) {
      LogUtils.e(e.toString());
      throw 'PLEASE LOG IN, REFRESH TOKEN IS CURRENTLY SUCK!';
      //throw UnauthorizedException();
    }
  }

  Future<Response<dynamic>> _retry(RequestOptions requestOptions) async {
    final options =
        Options(method: requestOptions.method, headers: requestOptions.headers);
    options.headers?['Authorization'] = '${sPref.accessToken!}';
    LogUtils.d(requestOptions.data.toString());
    LogUtils.d("Retrying ${options.method} ${requestOptions.path}");
    if (options.headers != null) {
      LogUtils.d("Headers: ${options.headers.toString()}");
    }

    return dio.request<dynamic>(
      requestOptions.path,
      data: requestOptions.data,
      queryParameters: requestOptions.queryParameters,
      options: options,
    );
  }
}
