import 'package:tinyguard/model/datasource/remote/entity/base_response_entity.dart';
import 'package:tinyguard/model/datasource/remote/entity/device_entity.dart';

class UserResetPasswordEntity extends BaseResponseApiEntity {
  UserResetPasswordEntity(super.body);

  factory UserResetPasswordEntity.fromJson(Map<String, dynamic> json) {
    return UserResetPasswordEntity(json);
  }

  @override
  void initialValue() {}
}
