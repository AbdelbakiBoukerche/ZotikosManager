import 'package:flutter/material.dart';
import 'package:zotikosmanager_ui/presentation/screens/devices_screen.dart';
import 'package:zotikosmanager_ui/presentation/screens/home_screen.dart';

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'ZotikosManager',
      // TODO Implement new navigation system
      initialRoute: HomeScreen.route,
      routes: {
        HomeScreen.route: (context) => HomeScreen(),
        DevicesScreen.route: (context) => DevicesScreen()
      },
    );
  }
}
