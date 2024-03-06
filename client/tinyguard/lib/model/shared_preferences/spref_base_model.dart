import 'package:shared_preferences/shared_preferences.dart';
import 'package:tinyguard/utils/log_utils.dart';

abstract class SPrefBaseModel {
  late SharedPreferences _prefs;

  Future<void> onInit() async {
    _prefs = await SharedPreferences.getInstance();
    LogUtils.i('SPrefs:onInit:$runtimeType');
  }

  bool getBool({required String key, required bool defaultValue}) {
    return _prefs.getBool(key) ?? defaultValue;
  }

  int getInt({required String key, required int defaultValue}) {
    return _prefs.getInt(key) ?? defaultValue;
  }

  double getDouble({required String key, required double defaultValue}) {
    return _prefs.getDouble(key) ?? defaultValue;
  }

  String? getString({required String key, required String? defaultValue}) {
    return _prefs.getString(key) ?? defaultValue;
  }

  List<String> getStringList({
    required String key,
    required List<String> defaultValue,
  }) {
    return _prefs.getStringList(key) ?? defaultValue;
  }

  Future<bool> setBool({required String key, required bool value}) {
    return _prefs.setBool(key, value);
  }

  Future<bool> setInt({required String key, required int value}) {
    return _prefs.setInt(key, value);
  }

  Future<bool> setDouble({required String key, required double value}) {
    return _prefs.setDouble(key, value);
  }

  Future<bool> setString({required String key, required String value}) {
    return _prefs.setString(key, value);
  }

  Future<bool> setStringList({
    required String key,
    required List<String> value,
  }) {
    return _prefs.setStringList(key, value);
  }

  Future<bool> remove({required String key}) {
    return _prefs.remove(key);
  }
}
