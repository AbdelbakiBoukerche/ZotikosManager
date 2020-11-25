import 'package:flutter/material.dart';
import 'package:zotikosmanager_ui/presentation/screens/devices.screen.dart';

import 'presentation/screens/home_screen.dart';

// ignore: must_be_immutable
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'ZotikosManager',
      initialRoute: HomeScreen.route,
      routes: {
        HomeScreen.route: (context) => HomeScreen(),
        DevicesScreen.route: (context) => DevicesScreen(),
      },
    );
  }
}
