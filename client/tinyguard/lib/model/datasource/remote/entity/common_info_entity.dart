class CommonInfoEntity {
  final int resultCode;
  final String messageCode;
  final String message;

  CommonInfoEntity({
    required this.resultCode,
    required this.messageCode,
    required this.message,
  });

  factory CommonInfoEntity.fromJson(Map<String, dynamic> json) {
    return CommonInfoEntity(
      resultCode: json['resultCode'] as int,
      messageCode: json['messageCode'] as String,
      message: json['message'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['resultCode'] = resultCode;
    data['messageCode'] = messageCode;
    data['message'] = message;
    return data;
  }
}
