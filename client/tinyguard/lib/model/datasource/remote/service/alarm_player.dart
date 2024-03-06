import 'dart:typed_data';

import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

class AlarmPlayer {
  static String path = 'assets/audio/baby-would-cry.mp3';
  static AudioPlayer player = AudioPlayer();
  static ByteData? _bytes;

  static Future<void> initialize() async {
    debugPrint("Alarm Player finished initializing");
  }

  static Future<void> play() async {
    _bytes = await rootBundle.load(path);
    if (_bytes != null) {
      Uint8List audioBytes = _bytes!.buffer
          .asUint8List(_bytes!.offsetInBytes, _bytes!.lengthInBytes);
      player.play(BytesSource(audioBytes));
    } else
      debugPrint("Audio is empty");
  }

  static Future<void> stop() async {
    debugPrint("Stop alarm");
    await player.stop();
  }

  static Future<void> setVolume(double volume) async {
    await player.setVolume(volume);
  }
}
