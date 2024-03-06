abstract class BaseResponseApiEntity {
  dynamic _result;
  String? message;
  String? error;

  BaseResponseApiEntity(dynamic body) {
    _result = _convertResponseJson(body);
    _setValueICommon();
    initialValue();
  }

  Map<String, dynamic> get body => _result as Map<String, dynamic>;

  void initialValue();

  void _setValueICommon() {
    message = body['message'] ?? null;
    error = body['error'] ?? null;
  }

  Map<String, dynamic> _convertResponseJson(dynamic responseJson) {
    return responseJson as Map<String, dynamic>;
  }
}
