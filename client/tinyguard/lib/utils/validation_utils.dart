import 'package:tinyguard/model/shared/constants.dart';

class ValidationUtils {
  ValidationUtils._();
  static bool isEmpty(String? s) {
    if (s == null) return true;
    return s == Constants.kEmptyString;
  }

  static bool isEmail(String email) {
    if (isEmpty(email)) {
      return false;
    }

    final emailRegexp = RegExp(
      r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]+$",
    );
    return emailRegexp.hasMatch(email);
  }

  static bool isValidPassword(String password) {
    if (isEmpty(password)) {
      return false;
    }

    if (password.length < Constants.kMinimumPasswordLength) {
      return false;
    }

    final passRegexp = RegExp(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$');
    return password.length >= Constants.kMinimumPasswordLength;
  }
}
