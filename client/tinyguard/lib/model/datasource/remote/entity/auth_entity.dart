import 'package:tinyguard/model/datasource/remote/entity/base_response_entity.dart';
import 'package:tinyguard/model/datasource/remote/entity/result_entity.dart';

class AuthEntity extends BaseResponseApiEntity {
  ResultEntity? result;

  AuthEntity(super.body);

  factory AuthEntity.fromJson(Map<String, dynamic> json) {
    return AuthEntity(json);
  }

  @override
  void initialValue() {
    result =
        body['result'] != null ? ResultEntity.fromJson(body['result']) : null;
  }
}
