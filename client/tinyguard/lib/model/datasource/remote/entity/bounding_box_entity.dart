class BoundingBoxEntity {
  final double x;
  final double y;
  final double w;
  final double h;
  final int label;
  final double confidence;

  BoundingBoxEntity({
    required this.x,
    required this.y,
    required this.w,
    required this.h,
    required this.label,
    required this.confidence,
  });

  factory BoundingBoxEntity.fromJson(Map<String, dynamic> json) {
    return BoundingBoxEntity(
      x: json["x"],
      y: json["y"],
      w: json["w"],
      h: json["h"],
      label: json["label"],
      confidence: json["confidence"].toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "x": x,
      "y": y,
      "w": w,
      "h": h,
      "label": label,
      "confidence": confidence,
    };
  }
}
