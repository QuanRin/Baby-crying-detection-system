import 'package:flutter/material.dart';
import 'package:tinyguard/model/datasource/remote/dto/user_register_credentials.dart';
import 'package:tinyguard/model/repository/user_repository.dart';
import 'package:tinyguard/utils/log_utils.dart';
import 'package:tinyguard/view_models/base_view_model.dart';

class RegisterViewModel extends BaseViewModel {
  final UserRepository userRepository;

  final emailController = TextEditingController()
    ..text = 'themysmine+acctest123@gmail.com';
  final phoneController = TextEditingController()..text = '00000000000000001';
  final passwordController = TextEditingController()..text = '1';

  RegisterViewModel({required this.userRepository});

  Future<void> onRegister({
    VoidCallback? onSuccess,
    VoidCallback? onFailure,
  }) async {
    try {
      debugPrint(emailController.text);
      debugPrint(passwordController.text);
      debugPrint(phoneController.text);
      await userRepository.register(
        UserRegisterCredentials(
          email: emailController.text,
          phone_number: phoneController.text,
          password: passwordController.text,
        ),
      );
      onSuccess?.call();
    } on Exception catch (error) {
      LogUtils.d('LOGIN ERROR:  $runtimeType => $error');
      onFailure?.call();
    }
  }
}
