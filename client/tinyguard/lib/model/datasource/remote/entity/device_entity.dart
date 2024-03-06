import 'package:tinyguard/model/datasource/remote/entity/base_response_entity.dart';
import 'package:tinyguard/model/datasource/remote/entity/user_entity.dart';

class DeviceEntity extends BaseResponseApiEntity {
  late String code;
  late UserEntity? user;

  DeviceEntity(super.body);

  factory DeviceEntity.fromJson(Map<String, dynamic> json) {
    return DeviceEntity(json);
  }

  @override
  void initialValue() {
    this.code = body['code'];
    this.user = null;
  }
}
