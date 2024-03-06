import 'package:flutter/material.dart';
import 'package:tinyguard/const/app_colors.dart';

class UIButtonTransparent extends StatelessWidget {
  final VoidCallback onTap;
  final Widget icon;

  const UIButtonTransparent({
    super.key,
    required this.onTap,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.8),
            borderRadius: BorderRadius.circular(100),
            border: Border.all(width: 1, color: Colors.white)),
        alignment: Alignment.center,
        padding: EdgeInsets.symmetric(vertical: 10, horizontal: 10),
        child: icon,
      ),
    );
  }
}
