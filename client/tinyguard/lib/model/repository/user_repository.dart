import 'package:tinyguard/model/datasource/remote/dto/user_credentials.dart';
import 'package:tinyguard/model/datasource/remote/dto/user_register_credentials.dart';
import 'package:tinyguard/model/datasource/remote/entity/user_entity.dart';
import 'package:tinyguard/model/datasource/remote/service/auth_api_service.dart';
import 'package:tinyguard/model/datasource/remote/entity/auth_entity.dart';
import 'package:tinyguard/model/datasource/remote/service/device_background_service.dart';
import 'package:tinyguard/model/repository/device_repository.dart';

abstract class UserRepository {
  Future<AuthEntity> login({UserCredentials? credentials = null});
  Future<UserEntity> register(UserRegisterCredentials credentials);
  User? get user;
}

class User {
  int id;
  String username;
  int? age;
  String phone_number;
  String email;
  String? role;
  List<Device> devices = [];

  User(this.id, this.username, this.age, this.phone_number, this.email,
      this.role, this.devices);

  factory User.fromEntity(UserEntity entity) {
    List<Device> devices =
        entity.devices.map((e) => Device.fromEntity(e)).toList();

    return User(entity.id!, entity.username!, entity.age, entity.phone_number!,
        entity.email!, entity.role, devices);
  }
}

class UserRepositoryImpl extends UserRepository {
  final AuthAPIService authAPIService;

  UserRepositoryImpl({
    required this.authAPIService,
  });

  User? user;

  @override
  Future<AuthEntity> login({UserCredentials? credentials = null}) async {
    return authAPIService.login(credentials: credentials).then((authEntity) {
      if (authEntity.result?.user != null)
        this.user = User.fromEntity(authEntity.result!.user!);
      for (var device in this.user!.devices) {
        DeviceBackgroundService.addDevice(device);
      }
      return authEntity;
    });
  }

  @override
  Future<UserEntity> register(UserRegisterCredentials credentials) async {
    return authAPIService.register(credentials);
  }
}
