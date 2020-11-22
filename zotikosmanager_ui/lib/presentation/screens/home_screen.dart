import 'package:flutter/material.dart';
import 'package:zotikosmanager_ui/presentation/screens/devices_screen.dart';

class HomeScreen extends StatelessWidget {
  static const String route = '/';
  const HomeScreen({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("ZotikosManager"),
        actions: [
          Container(
            margin: EdgeInsets.symmetric(horizontal: 10.0),
            child: IconButton(
              tooltip: "Show all Devices",
              icon: Icon(Icons.device_hub),
              onPressed: () =>
                  Navigator.of(context).pushNamed(DevicesScreen.route),
            ),
          ),
        ],
      ),
    );
  }
}
