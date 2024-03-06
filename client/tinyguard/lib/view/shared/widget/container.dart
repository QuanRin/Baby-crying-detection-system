import 'package:tinyguard/model/datasource/remote/service/esp32_cam.dart';

enum Component { esp32Camera, bluetoothUtil }

class ComponentContainer {
  static final ComponentContainer _instance = ComponentContainer._();

  ComponentContainer._();

  factory ComponentContainer() {
    return ComponentContainer._instance;
  }

  static ensureInit() async {
    await _instance._init();
  }

  _init() async {
    container = {
      Component.esp32Camera: await FakeEsp32Camera.create(),
      //Component.bluetoothUtil: ImplementedBluetoothUtil()
    };
  }

  late Map<Component, dynamic> container;

  get(Component component) {
    return container[component];
  }
}
