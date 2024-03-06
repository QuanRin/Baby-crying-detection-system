import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';

abstract class BluetoothUtil {
  List<BluetoothDiscoveryResult> get scanedAddresses;
  bool get isDiscovering;
  void scan(
      Function(BluetoothDiscoveryResult address)
          callback); // Start scanning and push address into stream, calling callback when an address is pushed

  Future<BluetoothConnection> pair(String address);
  void write(Uint8List data, {BluetoothConnection? connection});
  StreamSubscription<Uint8List> read(
      Function(Uint8List data, {BluetoothConnection? connection})
          callback); // Calling callback when receiving data from paired device
}

class BluetoothUtilNoPairedDevice implements Exception {
  String message;
  BluetoothUtilNoPairedDevice({this.message = ""});

  @override
  String toString() {
    return "BluetoothUtilNoPairedDevice: $message";
  }
}

class ImplementedBluetoothUtil implements BluetoothUtil {
  @override
  List<BluetoothDiscoveryResult> scanedAddresses = [];

  @override
  bool isDiscovering = false;

  BluetoothConnection? _connection;

  @override
  Future<BluetoothConnection> pair(String address) async {
    _connection = await BluetoothConnection.toAddress(address);
    return _connection!;
  }

  StreamSubscription? _scanSubcription;

  @override
  void scan(Function(BluetoothDiscoveryResult result) callback) {
    isDiscovering = true;
    _scanSubcription =
        FlutterBluetoothSerial.instance.startDiscovery().listen((result) {
      scanedAddresses.add(result);
      callback.call(result);
    });
    _scanSubcription?.onDone(() {
      isDiscovering = false;
    });
  }

  @override
  StreamSubscription<Uint8List> read(Function(Uint8List data) callback,
      {BluetoothConnection? connection}) {
    connection ??= _connection;
    if (connection == null) {
      throw BluetoothUtilNoPairedDevice();
    }
    return connection.input!.listen(callback);
  }

  @override
  void write(Uint8List data, {BluetoothConnection? connection}) {
    connection ??= _connection;
    if (connection == null) {
      throw BluetoothUtilNoPairedDevice();
    }
    connection.output.add(data);
  }
}
