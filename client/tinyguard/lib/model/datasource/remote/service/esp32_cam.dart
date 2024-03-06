import 'package:flutter/material.dart';

enum ConnectionStatus { disconnect, connecting, connected }

abstract class Esp32Camera {
  String? get streamingUrl;
  String? get bluetoothAddress;
  set bluetoothAddress(String? address);
  bool get isActive;

  ConnectionStatus get bluetoothStatus;
  ConnectionStatus get wifiStatus;

  Future<bool> connectBluetooth();
  bool disconnectBluetooth();
  Future<String> requestStreamingUrl();
  Future<bool> connectWifi(String ssid, String password);
  Future<bool> activateCamera();
  Future<bool> deactivateCamera();

  void onBluetoothConnect(Function(String address) callback);
  void onWifiConnect(Function(String ssid) callback);
  void onCameraActivate(Function() callback);
  void onCameraDeactivate(Function() callback);
}

class Esp32NoBluetoothConnectionException implements Exception {
  String message;
  Esp32NoBluetoothConnectionException(
      {this.message = "Please connect to bluetooth using connectBluetooth()"});

  @override
  String toString() {
    return "Esp32NoBluetoothConnectionException: $message";
  }
}

class Esp32NoWifiConnectionException implements Exception {
  String message;
  Esp32NoWifiConnectionException(
      {this.message =
          "Please connect camera to wifi using connectWifi(ssid, password)"});

  @override
  String toString() {
    return "Esp32NoWifiConnectionException: $message";
  }
}

class FakeEsp32Camera implements Esp32Camera {
  String _url;
  FakeEsp32Camera._()
      : _url = "",
        bluetoothStatus = ConnectionStatus.disconnect,
        wifiStatus = ConnectionStatus.disconnect,
        isActive = false;

  static create() async {
    var service = FakeEsp32Camera._();
    return service;
  }

  @override
  bool isActive;

  @override
  String get streamingUrl => _url;

  @override
  ConnectionStatus bluetoothStatus;

  @override
  String? bluetoothAddress;

  @override
  Future<bool> connectBluetooth() async {
    if (bluetoothAddress == null || bluetoothAddress!.isEmpty) return false;
    bluetoothStatus = ConnectionStatus.connecting;
    debugPrint("Connecting to camera through Bluetooth");
    await Future.delayed(const Duration(seconds: 3));
    debugPrint("Connect to camera successfully");
    bluetoothStatus = ConnectionStatus.connected;
    return true;
  }

  @override
  ConnectionStatus wifiStatus;

  @override
  Future<bool> connectWifi(String ssid, String password) async {
    if (bluetoothStatus != ConnectionStatus.connected) {
      return Future.error(Esp32NoBluetoothConnectionException());
    }
    wifiStatus = ConnectionStatus.connecting;
    debugPrint("Camera is connecting to Wifi");
    await Future.delayed(const Duration(seconds: 3));
    debugPrint("Camera's wifi connection is established");
    wifiStatus = ConnectionStatus.connected;
    return true;
  }

  @override
  Future<bool> activateCamera() async {
    if (bluetoothStatus != ConnectionStatus.connected) {
      return Future.error(Esp32NoBluetoothConnectionException());
    }
    _url = "http://uk.jokkmokk.jp/photo/nr4/latest.jpg";
    isActive = true;
    return true;
  }

  @override
  Future<bool> deactivateCamera() async {
    if (bluetoothStatus != ConnectionStatus.connected) {
      return Future.error(Esp32NoBluetoothConnectionException());
    }
    _url = "";
    isActive = false;
    return true;
  }

  @override
  bool disconnectBluetooth() {
    bluetoothAddress = "";
    bluetoothStatus = ConnectionStatus.disconnect;
    return true;
  }

  final List<Function(String address)> _bluetoothConnectCallbacks = [];
  final List<Function(String ssid)> _wifiConnectCallbacks = [];
  final List<Function()> _cameraActivateCallbacks = [];
  final List<Function()> _cameraDeactivateCallbacks = [];

  @override
  void onBluetoothConnect(Function(String address) callback) {
    _bluetoothConnectCallbacks.add(callback);
  }

  @override
  void onCameraActivate(Function() callback) {
    _cameraActivateCallbacks.add(callback);
  }

  @override
  void onCameraDeactivate(Function() callback) {
    _cameraDeactivateCallbacks.add(callback);
  }

  @override
  void onWifiConnect(Function(String ssid) callback) {
    _wifiConnectCallbacks.add(callback);
  }

  @override
  Future<String> requestStreamingUrl() async {
    if (bluetoothStatus != ConnectionStatus.connected) {
      return Future.error(Esp32NoBluetoothConnectionException());
    }
    if (wifiStatus != ConnectionStatus.connected) {
      return Future.error(Esp32NoWifiConnectionException());
    }
    return _url;
  }
}

class ImplementedEsp32Camera implements Esp32Camera {
  @override
  String? bluetoothAddress;

  @override
  Future<bool> activateCamera() {
    throw UnimplementedError();
  }

  @override
  ConnectionStatus get bluetoothStatus => throw UnimplementedError();

  @override
  Future<bool> connectBluetooth() {
    throw UnimplementedError();
  }

  @override
  Future<bool> connectWifi(String ssid, String password) {
    throw UnimplementedError();
  }

  @override
  Future<bool> deactivateCamera() {
    throw UnimplementedError();
  }

  @override
  bool disconnectBluetooth() {
    throw UnimplementedError();
  }

  @override
  bool get isActive => throw UnimplementedError();

  @override
  void onBluetoothConnect(Function(String address) callback) {}

  @override
  void onCameraActivate(Function() callback) {}

  @override
  void onCameraDeactivate(Function() callback) {}

  @override
  void onWifiConnect(Function(String ssid) callback) {}

  @override
  Future<String> requestStreamingUrl() {
    throw UnimplementedError();
  }

  @override
  String? get streamingUrl => throw UnimplementedError();

  @override
  ConnectionStatus get wifiStatus => throw UnimplementedError();
}
