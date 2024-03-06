import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:tinyguard/flavor_config.dart';

class IOSocketUtil {
  Function(dynamic) onConnect;
  Function(dynamic) onDisconnect;
  late IO.Socket socket;
  IOSocketUtil({required this.onConnect, required this.onDisconnect}) {
    socket = IO.io('${FlavorConfig.instance.baseURL}');
    socket.onConnect(onConnect);
    socket.onDisconnect(onDisconnect);
  }
}
