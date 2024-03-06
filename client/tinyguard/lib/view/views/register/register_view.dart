import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:get_it/get_it.dart';
import 'package:tinyguard/view/shared/already_have_an_account_acheck.dart';
import 'package:tinyguard/view/shared/background.dart';
import 'package:tinyguard/view/views/base/base_view.dart';
import 'package:tinyguard/view/views/base/responsive.dart';
import 'package:tinyguard/view_models/register_view_model.dart';
import 'components/sign_up_top_image.dart';

class RegisterView extends StatefulWidget {
  const RegisterView({Key? key}) : super(key: key);

  @override
  State<RegisterView> createState() => _RegisterViewState();
}

class _RegisterViewState extends State<RegisterView> {
  late RegisterViewModel viewModel;
  @override
  void initState() {
    viewModel = GetIt.instance.get<RegisterViewModel>();
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
                const SignUpScreenTopImage(),
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
                              cursorColor: Colors.black,
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
                              padding: const EdgeInsets.only(top: 16),
                              child: TextFormField(
                                textInputAction: TextInputAction.done,
                                obscureText: true,
                                cursorColor: Colors.black,
                                controller: viewModel.phoneController,
                                decoration: InputDecoration(
                                  hintText: "Your phone number",
                                  prefixIcon: Padding(
                                    padding: const EdgeInsets.all(16),
                                    child: Icon(Icons.phone),
                                  ),
                                ),
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.symmetric(vertical: 16),
                              child: TextFormField(
                                textInputAction: TextInputAction.done,
                                obscureText: true,
                                cursorColor: Colors.black,
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
                            const SizedBox(height: 8),
                            Hero(
                              tag: "login_btn",
                              child: ElevatedButton(
                                style: ButtonStyle(
                                    backgroundColor:
                                        MaterialStateProperty.all<Color>(
                                            Colors.deepPurpleAccent)),
                                onPressed: () {
                                  viewModel.onRegister(onSuccess: () {
                                    debugPrint('REGISTER SUCCESSFULLY');
                                  });
                                },
                                child: Text(
                                  "Sign up".toUpperCase(),
                                ),
                              ),
                            ),
                            const SizedBox(height: 16),
                            AlreadyHaveAnAccountCheck(
                              login: false,
                              press: () {
                                Get.back();
                              },
                            ),
                          ],
                        ),
                      ),
                    ),
                    Spacer(),
                  ],
                ),
                // const SocalSignUp()
              ],
            ),
          ),
        ),
      ),
    );
  }
}
