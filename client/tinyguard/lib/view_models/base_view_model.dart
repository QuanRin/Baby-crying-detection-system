import 'package:flutter/material.dart';

class BaseViewModel extends ChangeNotifier {
  void updateUI() {
    notifyListeners();
  }
}
