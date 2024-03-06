import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:get_it/get_it.dart';
import 'package:tinyguard/main_development.dart';
import 'package:tinyguard/view/shared/already_have_an_account_acheck.dart';
import 'package:tinyguard/view/shared/background.dart';
import 'package:tinyguard/view/views/base/base_view.dart';
import 'package:tinyguard/view/views/base/responsive.dart';
import 'package:tinyguard/view_models/log_in_view_model.dart';
import 'components/login_screen_top_image.dart';

class LoginScreen extends StatefulWidget {
  LoginScreen({Key? key}) : super(key: key);
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  late LogInViewModel viewModel;
  @override
  void initState() {
    viewModel = GetIt.instance.get<LogInViewModel>();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return BaseView(
      viewModel: viewModel,
      resizeToAvoidBottomInset: true,
      mobileBuilder: (context) => Background(
        child: SingleChildScrollView(
          child: Responsive(
            mobile: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                const LoginScreenTopImage(),
                Row(
                  children: [
                    Spacer(),
                    Expanded(
                      flex: 8,
                      child: Form(
                        child: Column(
                          children: [
                            TextFormField(
                              keyboardType: TextInputType.emailAddress,
                              textInputAction: TextInputAction.next,
                              onSaved: (email) {},
                              controller: viewModel.emailController,
                              decoration: InputDecoration(
                                hintText: "Your email",
                                prefixIcon: Padding(
                                  padding: const EdgeInsets.all(16),
                                  child: Icon(Icons.person),
                                ),
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.symmetric(vertical: 16),
                              child: TextFormField(
                                textInputAction: TextInputAction.done,
                                obscureText: true,
                                controller: viewModel.passwordController,
                                decoration: InputDecoration(
                                  hintText: "Your password",
                                  prefixIcon: Padding(
                                    padding: const EdgeInsets.all(16),
                                    child: Icon(Icons.lock),
                                  ),
                                ),
                              ),
                            ),
                            const SizedBox(height: 16),
                            Hero(
                              tag: "login_btn",
                              child: ElevatedButton(
                                style: ButtonStyle(
                                    backgroundColor:
                                        MaterialStateProperty.all<Color>(
                                            Colors.deepPurpleAccent)),
                                onPressed: () async {
                                  showDialog(
                                    context: context,
                                    barrierDismissible: false,
                                    builder: (BuildContext context) {
                                      return Center(
                                        child: CircularProgressIndicator(),
                                      );
                                    },
                                  );
                                  await viewModel.onLoginPressed(
                                    onSuccess: () {
                                      debugPrint('Login success');

                                      Navigator.pop(context);
                                      Get.toNamed(
                                        Routes.monitor,
                                      );
                                    },
                                    onFailure: (error) {
                                      return showDialog(
                                        context: context,
                                        builder: ((context) => AlertDialog(
                                              title: const Text('Error'),
                                              content: Text(
                                                error,
                                              ),
                                              actions: <Widget>[
                                                TextButton(
                                                  style: TextButton.styleFrom(
                                                    textStyle: Theme.of(context)
                                                        .textTheme
                                                        .labelLarge,
                                                  ),
                                                  child: const Text('Close'),
                                                  onPressed: () {
                                                    Navigator.of(context).pop();
                                                  },
                                                ),
                                              ],
                                            )),
                                      );
                                    },
                                  );
                                },
                                child: Text(
                                  "Login".toUpperCase(),
                                ),
                              ),
                            ),
                            const SizedBox(height: 16),
                            AlreadyHaveAnAccountCheck(
                              press: () => Get.toNamed(Routes.register),
                            ),
                          ],
                        ),
                      ),
                    ),
                    Spacer(),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
