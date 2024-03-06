import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:tinyguard/model/datasource/remote/service/alarm_player.dart';
import 'package:tinyguard/model/datasource/remote/service/device_background_service.dart';
import 'package:tinyguard/enums.dart';
import 'package:tinyguard/flavor_config.dart';
import 'package:tinyguard/locator_config.dart';
import 'package:tinyguard/view/views/first_setup_screen/ui/first_setup_screen.dart';
import 'package:tinyguard/view/views/monitor_screen/ui/monitor_screen.dart';
import 'package:tinyguard/view/views/login/login_screen.dart';
import 'package:tinyguard/view/views/register/register_view.dart';
import 'package:tinyguard/view/views/splash_screen/splash1_screen.dart';
import 'package:tinyguard/view/shared/widget/container.dart';

void main() async {
  await ComponentContainer.ensureInit();
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setEnabledSystemUIMode(
    SystemUiMode.leanBack,
    overlays: [
      SystemUiOverlay.bottom,
      SystemUiOverlay.top,
    ],
  );
  await setupLocator();
  FlavorConfig(
      baseApiUrl: "http://192.168.1.184:5000",
      flavor: Flavor.development,
      versionAPI: '/api/');
  await AlarmPlayer.initialize();
  await DeviceBackgroundService.initialized();
  //try {
  //  await getIt.get<UserRepository>().login();
  //  runApp(const MainApp(initRoute: Routes.firstSetup));
  //} on ApiException catch (e) {
  runApp(const MainApp());
  //}
}

class Routes {
  static const String splash1 = '/splash1';
  static const String firstSetup = '/firstsetup';
  static const String dashboard = '/dashboard';
  static const String monitor = '/monitor';
  static const String signIn = '/sign-in';
  static const String register = '/register';
  static final Map<String, Widget Function(BuildContext)> routes = {
    splash1: (context) {
      return Splash1Screen();
    },
    firstSetup: (context) {
      return FirstSetupScreen();
    },
    monitor: (context) {
      return MonitorScreen();
    },
    signIn: (context) {
      return LoginScreen();
    },
    register: (context) {
      return RegisterView();
    }
  };
}

class MainApp extends StatelessWidget {
  final String initRoute;
  const MainApp({super.key, this.initRoute = Routes.splash1});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      debugShowCheckedModeBanner: false,
      initialRoute: initRoute,
      routes: Routes.routes,
    );
  }
}
