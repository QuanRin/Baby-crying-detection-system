import 'package:flutter/material.dart';

class BoundingBox extends StatelessWidget {
  final double x;
  final double y;
  final double height;
  final double width;
  final bool isCrying;
  final double confidence;

  const BoundingBox({
    super.key,
    required this.x,
    required this.y,
    required this.height,
    required this.width,
    required this.isCrying,
    required this.confidence,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint(height.toString() + ", " + width.toString());
    debugPrint(y.toString() + ", " + x.toString());
    return Transform(
      transform:
          Matrix4.translationValues((y - height / 2), (x - width / 2), 0.0),
      child: Column(
        children: [
          Container(
            padding: EdgeInsets.symmetric(horizontal: 10, vertical: 5),
            decoration:
                BoxDecoration(color: isCrying ? Colors.red : Colors.green),
            child: Text(
              'Confidence: ${(confidence * 100).ceil()}%',
              style:
                  TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
            ),
          ),
          Container(
            height: height,
            width: width,
            decoration: BoxDecoration(
              border: Border.all(
                width: 5,
                color: isCrying ? Colors.red : Colors.green,
              ),
            ),
          ),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 10, vertical: 5),
            decoration:
                BoxDecoration(color: isCrying ? Colors.red : Colors.green),
            child: Text(
              isCrying ? 'Your baby is crying' : "Your baby is fine",
              style:
                  TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
            ),
          )
        ],
      ),
    );
  }
}
