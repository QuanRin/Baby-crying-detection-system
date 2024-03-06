import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:tinyguard/view/shared/ui_constant.dart';

class Responsive extends StatelessWidget {
  const Responsive({
    super.key,
    required this.mobile,
    this.tablet,
  });

  final Widget mobile;
  final Widget? tablet;

  @override
  Widget build(BuildContext context) {
    final Size size = MediaQuery.of(context).size;

    if (size.width >= UIConstants.kTabletWidth) {
      if (MediaQuery.of(context).orientation == Orientation.portrait) {
        ScreenUtil.init(
          context,
          designSize: const Size(
            UIConstants.kTabletWidth,
            UIConstants.kTabletHeight,
          ),
        );
      } else {
        ScreenUtil.init(
          context,
          designSize: const Size(
            UIConstants.kTabletHeight,
            UIConstants.kTabletWidth,
          ),
        );
      }

      return tablet ?? mobile;
    } else {
      if (MediaQuery.of(context).orientation == Orientation.portrait) {
        ScreenUtil.init(
          context,
          designSize: const Size(
            UIConstants.kDesignWidth,
            UIConstants.kDesignHeight,
          ),
        );
      } else {
        ScreenUtil.init(
          context,
          designSize: const Size(
            UIConstants.kDesignHeight,
            UIConstants.kDesignWidth,
          ),
        );
      }

      return mobile;
    }
  }
}
