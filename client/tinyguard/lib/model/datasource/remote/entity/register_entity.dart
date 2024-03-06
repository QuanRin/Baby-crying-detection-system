import 'package:tinyguard/model/datasource/remote/entity/base_response_entity.dart';
import 'package:tinyguard/model/datasource/remote/entity/user_entity.dart';

class RegisterEntity extends BaseResponseApiEntity {
  UserEntity? user;

  RegisterEntity(super.body);

  factory RegisterEntity.fromJson(Map<String, dynamic> json) {
    return RegisterEntity(json);
  }

  @override
  void initialValue() {
    user = body['result'] != null
        ? UserEntity.fromJson(body['result'] as Map<String, dynamic>)
        : null;
  }
}
