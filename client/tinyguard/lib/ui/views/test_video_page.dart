import 'package:flutter/material.dart';
import 'package:flutter_mjpeg/flutter_mjpeg.dart';
import 'package:tinyguard/model/datasource/remote/service/esp32_cam.dart';
import 'package:tinyguard/widget/container.dart';

class TestVideoPage extends StatefulWidget {
  const TestVideoPage({super.key});

  @override
  State<StatefulWidget> createState() => _TestVideoPageState();
}

class _TestVideoPageState extends State<TestVideoPage> {
  @override
  Widget build(BuildContext context) {
    final videoService =
        ComponentContainer().get(Component.esp32Camera) as Esp32Camera;
    videoService.bluetoothAddress = "55:65:AE:C8:CD:7C";
    return FutureBuilder(
      future: videoService
          .connectBluetooth()
          .then((value) => videoService.connectWifi("A", "B").then((value) =>
              videoService
                  .activateCamera()
                  .then((value) => videoService.requestStreamingUrl())))
          .onError((error, stackTrace) {
        debugPrint(error.toString());
        return "";
      }),
      builder: (context, snapshot) {
        if (snapshot.data == null) {
          return const CircularProgressIndicator();
        }
        if (snapshot.data!.isEmpty) {
          return const Center(
            child: Text("Camera not found"),
          );
        }
        final url = snapshot.data!;
        debugPrint("Camera streaming at: $url");
        return Mjpeg(
          stream: url,
          isLive: true,
        );
      },
    );
  }
}
