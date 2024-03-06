import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:tinyguard/view/views/base/base_view.dart';
import 'package:tinyguard/view/shared/widget/app_text_field.dart';
import 'package:tinyguard/view/shared/widget/ui_header.dart';
import '../../../../main_development.dart';

class FirstSetupScreen extends StatefulWidget {
  const FirstSetupScreen({super.key});

  @override
  State<FirstSetupScreen> createState() => _FirstSetupScreenState();
}

class _FirstSetupScreenState extends State<FirstSetupScreen> {
  @override
  void initState() {
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
    ]);
    super.initState();
  }

  @override
  void dispose() {
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
    ]);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.leanBack, overlays: [
      SystemUiOverlay.bottom,
      SystemUiOverlay.top,
    ]);

    final urlController = TextEditingController();
    return BaseView(mobileBuilder: (context) {
      return GestureDetector(
        onTap: () => FocusManager.instance.primaryFocus?.unfocus(),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            UIHeader(
              title: 'First setup ',
            ),
            SizedBox(
              height: 50,
            ),
            Padding(
              padding: EdgeInsets.symmetric(horizontal: 20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "Url please:",
                    style: TextStyle(
                      fontSize: 15,
                      color: Colors.black,
                    ),
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  AppTextField(
                    onChanged: (_) {},
                    controller: urlController,
                    radius: 10,
                    backgroundColor: Colors.grey[100],
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  GestureDetector(
                    onTap: () => Get.toNamed(
                      Routes.monitor,
                      arguments: urlController.text,
                    ),
                    child: Container(
                      width: MediaQuery.of(context).size.width,
                      padding: EdgeInsets.all(15),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(15),
                        color: Colors.deepPurpleAccent,
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            "Get started ",
                            textAlign: TextAlign.center,
                            style: TextStyle(
                                letterSpacing: 1,
                                fontSize: 19,
                                color: Colors.white,
                                fontFamily: "Roboto",
                                fontWeight: FontWeight.bold),
                          ),
                          Icon(
                            Icons.navigate_next,
                            color: Colors.white,
                            size: 30,
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      );
    });
  }
}
