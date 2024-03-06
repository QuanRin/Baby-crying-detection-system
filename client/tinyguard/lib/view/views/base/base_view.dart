import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:tinyguard/view/views/base/responsive.dart';
import 'package:tinyguard/view_models/base_view_model.dart';

class BaseView<VM extends BaseViewModel?> extends StatelessWidget {
  final Color? backgroundColor;
  final Widget Function(BuildContext)? bottomNavigationBuilder;
  final VM? viewModel;
  final Widget Function(BuildContext) mobileBuilder;
  final Widget Function(BuildContext)? desktopBuilder;
  final Widget Function(BuildContext)? tabletBuilder;
  final bool resizeToAvoidBottomInset;
  final PreferredSizeWidget? appBar;
  final bool onWillPop;

  const BaseView({
    super.key,
    this.viewModel,
    this.backgroundColor,
    this.bottomNavigationBuilder,
    required this.mobileBuilder,
    this.desktopBuilder,
    this.tabletBuilder,
    this.resizeToAvoidBottomInset = false,
    this.appBar,
    this.onWillPop = false,
  });

  @override
  Widget build(BuildContext context) {
    if (viewModel != null) {
      return ChangeNotifierProvider.value(
        value: viewModel,
        builder: (ctx, _) {
          return _buildBody(ctx);
        },
      );
    } else {
      return _buildBody(context);
    }
  }

  Widget _buildBody(BuildContext context) {
    return WillPopScope(
      onWillPop: () => Future.value(onWillPop),
      child: Scaffold(
        resizeToAvoidBottomInset: resizeToAvoidBottomInset,
        appBar: appBar,
        body:
            // OrientationBuilder(
            //   builder: (ctx, __) {
            //     return
            Responsive(
          mobile: mobileBuilder.call(context),
          tablet: tabletBuilder?.call(context),
        ),
        //   },
        // ),
        bottomNavigationBar: bottomNavigationBuilder?.call(context),
        backgroundColor: backgroundColor,
      ),
    );
  }
}
