import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:tinyguard/enums.dart';
import 'package:tinyguard/flavor_config.dart';
import 'package:tinyguard/ui/views/first_setup_screen/ui/first_setup_screen.dart';

import 'package:tinyguard/ui/views/monitor_screen/ui/monitor_screen.dart';
import 'package:tinyguard/ui/views/splash_screen/splash1_screen.dart';
import 'package:tinyguard/widget/container.dart';

void main() async {
  await ComponentContainer.ensureInit();
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setEnabledSystemUIMode(SystemUiMode.leanBack, overlays: [
    SystemUiOverlay.bottom,
    SystemUiOverlay.top,
  ]);
  FlavorConfig(baseApiUrl: "", flavor: Flavor.production, versionAPI: 'v1');
  runApp(const MainApp());
}

class Routes {
  static const String splash1 = '/splash1';
  static const String splash2 = '/splash2';
  static const String splash3 = '/splash3';

  static const String firstSetup = '/firstsetup';
  static const String dashboard = '/dashboard';
  static const String monitor = '/monitor';
  static final Map<String, Widget Function(BuildContext)> routes = {
    splash1: (context) {
      return Splash1Screen();
    },
    firstSetup: (context) {
      return FirstSetupScreen();
    },
    monitor: (context) {
      return MonitorScreen();
    }
  };
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      debugShowCheckedModeBanner: false,
      initialRoute: Routes.splash1,
      routes: Routes.routes,
    );
  }
}
