import 'package:flutter/material.dart';
import 'package:get/get.dart';

class UIHeader extends StatelessWidget {
  final VoidCallback? onPressed;
  final String? title;
  const UIHeader({super.key, this.onPressed, this.title});

  @override
  Widget build(BuildContext context) {
    return Container(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          SizedBox(
            width: 80,
            child: Row(
              children: [
                IconButton(
                    onPressed: () => onPressed ?? Get.back(),
                    icon: Icon(
                      Icons.chevron_left,
                      size: 40,
                    )),
              ],
            ),
          ),
          Center(
              child: Text(
            title ?? '',
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 22),
          )),
          SizedBox(
            width: 80,
          )
        ],
      ),
    );
  }
}
