import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

import 'package:zotikosmanager_ui/logic/models/device.dart';

abstract class ZotikosRepository {
  static Future<List<Device>> getDevicesList() async {
    final response = await http.get("http://127.0.0.1:5000/devices");
    if (response.statusCode == 200) {
      List<Device> devices = jsonDecode(response.body)["devices"]
          .map((deviceJson) => Device.fromJson(deviceJson))
          .toList()
          .cast<Device>();
      return devices;
    } else {
      print("Cannot get devices from url: http://127.0.0.1:5000/devices");
      return [];
    }
  }
}
