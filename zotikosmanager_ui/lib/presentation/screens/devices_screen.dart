import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:zotikosmanager_ui/models/device.dart';

class DevicesScreen extends StatefulWidget {
  static const String route = '/devices';
  DevicesScreen({Key key}) : super(key: key);

  @override
  _DevicesScreenState createState() => _DevicesScreenState();
}

class _DevicesScreenState extends State<DevicesScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Devices"),
      ),
      body: Center(
        child: FutureBuilder(
          future: _fetchDevices(),
          builder: (BuildContext context, AsyncSnapshot snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return CircularProgressIndicator();
            }
            if (snapshot.connectionState == ConnectionState.done) {
              if (!snapshot.hasData) {
                return Text("no data available");
              } else if (snapshot.hasData) {
                print(snapshot.data[0].toString());
                return _getListView(snapshot.data);
              }
            }

            return Container();
          },
        ),
      ),
    );
  }

  Widget _deviceListTile(Device device) {
    return ListTile(
      leading: device.availability
          ? Icon(
              Icons.check,
              color: Colors.green,
            )
          : Icon(
              Icons.close,
              color: Colors.red,
            ),
      title: Text("${device.hostname}\n${device.name}"),
      subtitle: Text(device.ip_address),
      trailing: IconButton(
        icon: Icon(Icons.keyboard_arrow_right),
        onPressed: () {},
        tooltip: "Show more information",
      ),
    );
  }

  Widget _getListView(devices) {
    return ListView.builder(
      itemCount: devices.length,
      itemBuilder: (BuildContext context, int index) {
        return _deviceListTile(devices[index]);
      },
    );
  }

  Future<List<Device>> _fetchDevices() async {
    final resp = await http.get("http://127.0.0.1:5000/devices");
    if (resp.statusCode == 200) {
      List<Device> devices = jsonDecode(resp.body)["devices"]
          .map((deviceJson) => Device.fromJson(deviceJson))
          .toList()
          .cast<Device>();
      return devices;
    } else {
      return [];
    }
  }
}
