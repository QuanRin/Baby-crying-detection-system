import 'package:card_swiper/card_swiper.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:flutter/services.dart';
import 'package:tinyguard/main_development.dart';
import 'package:tinyguard/view/views/base/base_view.dart';

class Splash1Screen extends StatefulWidget {
  Splash1Screen({super.key});

  @override
  State<Splash1Screen> createState() => _Splash1ScreenState();
}

class _Splash1ScreenState extends State<Splash1Screen> {
  List<String> babyCard = [
    "assets/images/baby1.png",
    "assets/images/baby2.png",
    "assets/images/baby3.png"
  ];
  @override
  void initState() {
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
    ]);

    super.initState();
  }

  @override
  void dispose() {
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
    ]);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BaseView(mobileBuilder: (context) {
      return GestureDetector(
        onTap: () => FocusManager.instance.primaryFocus?.unfocus(),
        child: Container(
          child: Column(
            children: [
              Expanded(
                flex: 7,
                child: Container(
                  width: MediaQuery.of(context).size.width,
                  child: Swiper(
                    itemBuilder: (BuildContext context, int index) {
                      return Container(
                        margin:
                            EdgeInsets.symmetric(horizontal: 25, vertical: 25),
                        decoration: BoxDecoration(
                          color: Colors.transparent,
                          borderRadius: BorderRadius.circular(41),
                          image: DecorationImage(
                            image: AssetImage(
                              babyCard[index],
                            ),
                          ),
                        ),
                      );
                    },
                    pagination: SwiperPagination(
                      alignment: Alignment
                          .bottomCenter, // Align the dots at the bottom
                      margin: EdgeInsets.only(
                          bottom: 0), // Add some margin to the dots
                      builder: DotSwiperPaginationBuilder(
                        color: Colors.grey[300], // Color of inactive dots
                        activeColor:
                            Colors.deepPurpleAccent, // Color of active dot
                        size: 10, // Size of dots
                        activeSize: 13, // Size of the active dot
                      ),
                    ),
                    itemHeight: 100,
                    itemWidth: 100,
                    itemCount: 3,
                    autoplay: true,
                    autoplayDelay: 3000,
                    loop: true,
                    onIndexChanged: (value) {},
                  ),
                ),
              ),
              Expanded(
                flex: 6,
                child: Container(
                  padding: EdgeInsets.only(
                    right: 30,
                    left: 30,
                    bottom: 80,
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      Text(
                        "Track everything!",
                        style: TextStyle(
                          letterSpacing: 3,
                          fontSize: 30,
                          color: Colors.grey[800],
                          fontFamily: "Roboto",
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      Text(
                        "Hundreds of activities for Physical, Cognitive, Speech and Social-Emotional Development",
                        maxLines: 2,
                        textAlign: TextAlign.center,
                        style: TextStyle(
                            letterSpacing: 1,
                            fontSize: 16,
                            color: Colors.grey[700],
                            fontFamily: "Roboto",
                            fontWeight: FontWeight.w400),
                      ),
                      GestureDetector(
                        onTap: () => Get.toNamed(Routes.signIn),
                        child: Container(
                          width: MediaQuery.of(context).size.width / 1.4,
                          padding: EdgeInsets.all(15),
                          decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(15),
                              color: Colors.deepPurpleAccent),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text(
                                "Get started ",
                                textAlign: TextAlign.center,
                                style: TextStyle(
                                    letterSpacing: 1,
                                    fontSize: 20,
                                    color: Colors.grey[100],
                                    fontFamily: "Roboto",
                                    fontWeight: FontWeight.bold),
                              ),
                              Icon(
                                Icons.navigate_next,
                                color: Colors.white,
                                size: 30,
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              )
            ],
          ),
        ),
      );
    });
  }
}
