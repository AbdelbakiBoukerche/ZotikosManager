import 'package:flutter/material.dart';
import 'package:zotikosmanager_ui/presentation/screens/devices.screen.dart';

class HomeScreen extends StatefulWidget {
  static const String route = '/';
  HomeScreen({Key key}) : super(key: key);

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("ZotikosManager"),
        actions: [
          IconButton(
            icon: Icon(Icons.device_hub),
            tooltip: "Show all devices",
            onPressed: () => Navigator.pushNamed(context, DevicesScreen.route),
          ),
        ],
      ),
      body: Center(
        child: Text("HOME PAGE"),
      ),
    );
  }
}
