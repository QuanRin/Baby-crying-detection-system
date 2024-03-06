import 'package:tinyguard/model/datasource/remote/entity/audio_predict_entity.dart';
import 'package:tinyguard/model/datasource/remote/entity/image_predict_entity.dart';

class Predict {
  ImagePredict image_predict;
  AudioPredict audio_predict;
  bool is_crying;

  Predict(this.image_predict, this.audio_predict, this.is_crying);

  factory Predict.fromJson(data) {
    return Predict(ImagePredict.fromJson(data["image_prediction"]),
        AudioPredict.fromJson(data["audio_prediction"]), data["is_crying"]);
  }
}
