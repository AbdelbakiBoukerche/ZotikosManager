import 'dart:async';

import 'package:flutter/material.dart';
import 'package:zotikosmanager_ui/logic/models/device.dart';
import 'package:zotikosmanager_ui/repositories/zotikos_repository.dart';

class DevicesScreen extends StatefulWidget {
  static const String route = '/devices';
  DevicesScreen({Key key}) : super(key: key);

  @override
  _DevicesScreenState createState() => _DevicesScreenState();
}

class _DevicesScreenState extends State<DevicesScreen> {
  Timer _timer;
  var _streamListDevice = StreamController<List<Device>>();

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(Duration(seconds: 5), (timer) async {
      final devices = await ZotikosRepository.getDevicesList();
      _streamListDevice.add(devices);
    });
  }

  @override
  void dispose() {
    _streamListDevice.close();
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Devices"),
      ),
      body: Center(
        child: StreamBuilder<List<Device>>(
          stream: _streamListDevice.stream,
          builder:
              (BuildContext context, AsyncSnapshot<List<Device>> snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return CircularProgressIndicator();
            }
            if (snapshot.connectionState == ConnectionState.active) {
              if (snapshot.hasData) {
                return ListView.builder(
                  itemCount: snapshot.data.length,
                  itemBuilder: (BuildContext context, int index) {
                    return _buildDeviceListTile(device: snapshot.data[index]);
                  },
                );
              }
              if (!snapshot.hasData) {
                return Text("No data available");
              }
            }
          },
        ),
      ),
    );
  }

  Widget _buildDeviceListTile({@required Device device}) {
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
      subtitle: Text("${device.ip_address}"),
      trailing: IconButton(
        icon: Icon(Icons.keyboard_arrow_right),
        tooltip: "Show more information",
        onPressed: () {},
      ),
    );
  }
}
