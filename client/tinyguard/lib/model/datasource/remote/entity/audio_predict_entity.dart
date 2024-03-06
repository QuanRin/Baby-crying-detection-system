class AudioPredict {
  final String prediction;
  final double score;
  final bool is_crying;

  AudioPredict(this.prediction, this.score, this.is_crying);

  factory AudioPredict.fromJson(Map<String, dynamic> json,
      {bool is_crying = false}) {
    return AudioPredict(json['prediction'], json["score"], is_crying);
  }
}
