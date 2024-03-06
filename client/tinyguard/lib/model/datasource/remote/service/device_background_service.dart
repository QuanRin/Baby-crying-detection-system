import 'dart:async';
import 'dart:io';
import 'dart:ui';
import 'package:flutter_background_service/flutter_background_service.dart';
import 'package:flutter_background_service_android/flutter_background_service_android.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:intl/intl.dart';
import 'package:tinyguard/model/datasource/remote/entity/audio_predict_entity.dart';
import 'package:tinyguard/model/datasource/remote/entity/image_predict_entity.dart';
import 'package:tinyguard/model/datasource/remote/entity/predict_entity.dart';
import 'package:tinyguard/model/datasource/remote/service/alarm_player.dart';
import 'package:tinyguard/model/repository/device_repository.dart';

// @pragma("vm:entry-point")
class DeviceBackgroundService {
  static final FlutterBackgroundService service = FlutterBackgroundService();

  static final AndroidNotificationChannel channel = AndroidNotificationChannel(
    'tinyguard_foreground_service', // id
    'TinyGuard Foreground Service', // title
    description:
        'This channel is used for important notifications.', // description
    importance: Importance.high, // importance must be at low or higher level
  );

  static final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
      FlutterLocalNotificationsPlugin();

  static final List<Device> _devices = [];

  static final List<StreamSubscription> _streams = [];

  static int last = 0;
  static bool isCameraCrying = false;
  static bool isMicroCrying = false;
  static const int interval = 10000;

  static bool isCrying = false;

  static void onCameraPredict(ImagePredict predict) {
    if (isCameraCrying &&
        DateTime.now().millisecondsSinceEpoch - last >= interval) {
      isCameraCrying = false;
    }
    if (predict.is_crying && !isCameraCrying) {
      last = DateTime.now().millisecondsSinceEpoch;
      isCameraCrying = true;
      service.invoke(
        "onCameraBabyCrying",
        {"id": "test"},
      );
    } else if (!predict.is_crying && isCameraCrying) {
      isCameraCrying = false;
    }
  }

  static void onMicroPredict(AudioPredict predict) {
    if (isMicroCrying &&
        DateTime.now().millisecondsSinceEpoch - last >= interval) {
      isMicroCrying = false;
    }
    if (predict.prediction == "Cry" && !isMicroCrying) {
      last = DateTime.now().millisecondsSinceEpoch;
      isMicroCrying = true;
      service.invoke(
        "onMicroBabyCrying",
        {"id": "test"},
      );
    } else if (predict.prediction != "Cry" && isMicroCrying) {
      isMicroCrying = false;
    }
  }

  static void onCryingPredict(Predict predict) {
    if (predict.is_crying) service.invoke("startWarning");
  }

  static void addDevice(Device device) {
    _devices.add(device);
    _streams.add(device.image_predicts.stream.listen(onCameraPredict));
    _streams.add(device.predicts.stream.listen(onCryingPredict));
    _streams.add(device.audio_predicts.stream.listen(onMicroPredict));
  }

  static void onReceiveResponse(NotificationResponse details) {
    print(details.actionId);
    print(details.notificationResponseType);
    switch (details.notificationResponseType) {
      case NotificationResponseType.selectedNotification:
        service.invoke("stopWarning");
        break;

      case NotificationResponseType.selectedNotificationAction:
        switch (details.actionId) {
          case 'baby_crying_confirm':
            // Stop music
            service.invoke("stopWarning");
            break;
        }
        break;
      default:
        break;
    }
  }

  static Future<void> initialized() async {
    if (Platform.isIOS || Platform.isAndroid) {
      await flutterLocalNotificationsPlugin.initialize(
        const InitializationSettings(
          iOS: DarwinInitializationSettings(),
          android: AndroidInitializationSettings('ic_bg_service_small'),
        ),
        onDidReceiveNotificationResponse: onReceiveResponse,
        onDidReceiveBackgroundNotificationResponse: onReceiveResponse,
      );
    }

    await flutterLocalNotificationsPlugin
        .resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>()
        ?.createNotificationChannel(channel);
    await service.configure(
      androidConfiguration: AndroidConfiguration(
        // this will be executed when app is in foreground or background in separated isolate
        onStart: _onStart,

        // auto start service
        autoStart: true,
        isForegroundMode: true,

        notificationChannelId: 'tinyguard_foreground_service',
        initialNotificationTitle: 'TinyGuard Alert Service',
        initialNotificationContent: 'Welcome to TinyGuard',
        foregroundServiceNotificationId: 888,
      ),
      iosConfiguration: IosConfiguration(
        // auto start service
        autoStart: true,

        // this will be executed when app is in foreground in separated isolate
        onForeground: _onStart,
      ),
    );
  }

  static void _onStart(ServiceInstance service) {
    DartPluginRegistrant.ensureInitialized();
    if (service is AndroidServiceInstance) {
      service.setAsForegroundService();
    }

    // Timer.periodic(Duration(seconds: 1), (timer) {
    //   flutterLocalNotificationsPlugin.show(
    //       888,
    //       'TinyGuard Alert',
    //       '${_streams.length}' + '\n$last',
    //       NotificationDetails(
    //         android: AndroidNotificationDetails(
    //             'tinyguard_foreground', 'TinyGuard Foreground Service',
    //             icon: 'ic_bg_service_small',
    //             ongoing: true,
    //             actions: [
    //               AndroidNotificationAction("baby_crying_confirm", "Confirm",
    //                   showsUserInterface: true)
    //             ],
    //             subText:
    //                 "Camera with code: 'test' detected your baby is crying"),
    //       ));
    // });

    service.on("stopWarning").listen((event) async {
      await AlarmPlayer.stop();
    });

    service.on("crying").listen((event) {
      isCrying = true;
    });

    service.on("mute").listen((event) async {
      await AlarmPlayer.setVolume(0.0);
    });

    service.on("unmute").listen((event) async {
      await AlarmPlayer.setVolume(1.0);
    });

    service.on("startWarning").listen((event) {
      AlarmPlayer.play();
    });

    service.on("onCameraBabyCrying").listen((data) async {
      last = DateTime.now().millisecondsSinceEpoch;
      //AlarmPlayer.play();
      final code = data?['id'] ?? '';

      if (data != null)
        flutterLocalNotificationsPlugin.show(
          888,
          'TinyGuard Alert',
          'The camera has detected that your baby is crying!\n' +
              DateFormat("yyyy-MM-dd h:mm:ss a").format(DateTime.now()),
          NotificationDetails(
            android: AndroidNotificationDetails(
              'tinyguard_foreground',
              'TinyGuard Foreground Service',
              icon: 'ic_bg_service_small',
              actions: [
                AndroidNotificationAction("baby_crying_confirm", "Confirm",
                    showsUserInterface: true)
              ],
              subText: "Camera $code",
              autoCancel: true,
              styleInformation: BigTextStyleInformation(
                  'The camera has detected that your baby is crying!\n' +
                      DateFormat("yyyy-MM-dd h:mm:ss a")
                          .format(DateTime.now())),
            ),
          ),
        );
    });

    service.on("onMicroBabyCrying").listen((data) async {
      last = DateTime.now().millisecondsSinceEpoch;
      final code = data?['id'] ?? '';

      if (data != null)
        flutterLocalNotificationsPlugin.show(
          888,
          'TinyGuard Alert',
          'The baby crying can be heard!\n' +
              DateFormat("yyyy-MM-dd h:mm:ss a").format(DateTime.now()),
          NotificationDetails(
            android: AndroidNotificationDetails(
              'tinyguard_foreground',
              'TinyGuard Foreground Service',
              icon: 'ic_bg_service_small',
              actions: [
                AndroidNotificationAction("baby_crying_confirm", "Confirm",
                    showsUserInterface: true)
              ],
              subText: "Camera $code",
              autoCancel: true,
              styleInformation: BigTextStyleInformation(
                  'The baby crying can be heard!\n' +
                      DateFormat("yyyy-MM-dd h:mm:ss a")
                          .format(DateTime.now())),
            ),
          ),
        );
    });
  }
}
