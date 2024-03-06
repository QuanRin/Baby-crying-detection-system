import 'package:tinyguard/model/datasource/remote/entity/bounding_box_entity.dart';

class ImagePredict {
  final List<BoundingBoxEntity> bboxes;
  final bool is_crying;

  ImagePredict({
    required this.bboxes,
    required this.is_crying,
  });

  factory ImagePredict.fromJson(Map<String, dynamic> json) {
    final List<BoundingBoxEntity> bboxes = [];
    for (var element in json['bboxes']) {
      bboxes.add(
        BoundingBoxEntity.fromJson(element),
      );
    }
    return ImagePredict(
      bboxes: bboxes,
      is_crying: json["is_crying"],
    );
  }
}
