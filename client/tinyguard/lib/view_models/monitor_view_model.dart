import 'package:flutter/material.dart';
import 'package:tinyguard/model/datasource/remote/service/device_background_service.dart';
import 'package:tinyguard/model/repository/user_repository.dart';
import 'package:tinyguard/view_models/base_view_model.dart';
import 'package:tinyguard/view/shared/widget/bounding_box.dart';

class MonitorViewModel extends BaseViewModel {
  final UserRepository userRepository;
  late List<BoundingBox> listBoundingBox;

  bool isCrying = false;

  bool isExpanding = false;

  bool isPredicting = true;

  bool isMute = false;

  void setExpand() {
    isExpanding = !isExpanding;
    updateUI();
  }

  void setPredicting() {
    isPredicting = !isPredicting;
    debugPrint("PREDICT STATUS : " + isPredicting.toString());
    updateUI();
  }

  void setMute() {
    if (isMute == true) {
      isMute = false;
      DeviceBackgroundService.service.invoke("unmute");
    } else {
      isMute = true;
      DeviceBackgroundService.service.invoke("mute");
    }
    updateUI();
  }

  void stopWarning() {
    DeviceBackgroundService.service.invoke("stopWarning");
    updateUI();
  }

  void checkCrying() {}

  MonitorViewModel({required this.userRepository});
}
