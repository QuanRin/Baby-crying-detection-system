import 'package:tinyguard/model/datasource/remote/entity/base_response_entity.dart';
import 'package:tinyguard/model/datasource/remote/entity/device_entity.dart';

class UserEntity extends BaseResponseApiEntity {
  int? id;
  String? username;
  int? age;
  String? phone_number;
  String? email;
  String? role;
  List<DeviceEntity> devices = [];

  UserEntity(super.body);

  factory UserEntity.fromJson(Map<String, dynamic> json) {
    return UserEntity(json);
  }

  @override
  void initialValue() {
    this.devices = [];
    this.id = body['id'];
    this.username = body['username'];
    this.email = body['email'];
    this.phone_number = body['phone_number'];
    this.role = body['role'];
    if (body['devices'] != null) {
      for (var element in body['devices']) {
        this.devices.add(DeviceEntity(element)..user = this);
      }
    }
  }
}
