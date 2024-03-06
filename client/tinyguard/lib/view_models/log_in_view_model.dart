import 'package:flutter/material.dart';
import 'package:tinyguard/model/datasource/remote/dto/user_credentials.dart';
import 'package:tinyguard/model/datasource/remote/entity/auth_entity.dart';
import 'package:tinyguard/model/repository/user_repository.dart';
import 'package:tinyguard/model/shared/constants.dart';
import 'package:tinyguard/model/shared_preferences/spref_auth_model.dart';
import 'package:tinyguard/utils/log_utils.dart';
import 'package:tinyguard/view_models/base_view_model.dart';

class LogInViewModel extends BaseViewModel {
  final UserRepository userRepository;
  final SPrefAuthModel sPref;

  final emailController = TextEditingController()
    ..text = 'themysmine@gmail.com';
  final passwordController = TextEditingController()..text = 'ComTMM0112';

  LogInViewModel({
    required this.userRepository,
    required this.sPref,
  });

  Future<void> onLoginPressed({
    VoidCallback? onSuccess,
    Function(String)? onFailure,
  }) async {
    try {
      debugPrint(emailController.text);
      debugPrint(passwordController.text);
      final entity = await userRepository.login(
        credentials: UserCredentials(
          email: emailController.text,
          password: passwordController.text,
        ),
      );
      onSuccessLogin(entity, onSuccess);
    } on Exception catch (error) {
      LogUtils.d('LOGIN ERROR:  $runtimeType => $error');
      onFailure?.call(error.toString());
    }
  }

  Future<void> onSuccessLogin(
    AuthEntity entity,
    VoidCallback? onSuccess,
  ) async {
    await sPref.setAccessToken(
      value: entity.result?.accessToken ?? Constants.kEmptyString,
    );
    await sPref.setRefreshToken(
      value: entity.result?.refreshToken ?? Constants.kEmptyString,
    );
    debugPrint('Access Token: ${sPref.accessToken}');
    debugPrint('Refresh Token: ${sPref.refreshToken}');
    onSuccess?.call();
  }
}
