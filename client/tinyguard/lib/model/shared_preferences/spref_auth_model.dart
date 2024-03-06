import 'package:tinyguard/model/shared_preferences/spref_base_model.dart';

class SPrefAuthModel extends SPrefBaseModel {
  static const String kAccessToken = 'KEY_ACCESS_TOKEN';
  static const String kRefreshToken = 'KEY_REFRESH_TOKEN';

  static SPrefAuthModel? _instance;

  SPrefAuthModel._();

  factory SPrefAuthModel() => _instance ??= SPrefAuthModel._();

  String? get accessToken {
    return getString(key: kAccessToken, defaultValue: null);
  }

  Future<bool> setAccessToken({required String value}) {
    return setString(key: kAccessToken, value: value);
  }

  String? get refreshToken {
    return getString(key: kRefreshToken, defaultValue: null);
  }

  Future<bool> setRefreshToken({required String value}) {
    return setString(key: kRefreshToken, value: value);
  }
}
