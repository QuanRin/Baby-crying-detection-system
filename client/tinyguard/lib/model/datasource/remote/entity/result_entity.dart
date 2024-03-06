import 'package:tinyguard/model/datasource/remote/entity/user_entity.dart';

class ResultEntity {
  final String? accessToken;
  final String? refreshToken;
  UserEntity? user;

  ResultEntity({this.accessToken, this.refreshToken, this.user});

  factory ResultEntity.fromJson(Map<String, dynamic> json) {
    return ResultEntity(
        accessToken: json['access_token'] as String?,
        refreshToken: json['refresh_token'] as String?,
        user: json['user'] != null
            ? UserEntity.fromJson(json['user'] as Map<String, dynamic>)
            : null);
  }
}
