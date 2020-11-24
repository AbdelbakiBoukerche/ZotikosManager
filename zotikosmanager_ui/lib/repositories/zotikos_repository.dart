import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

import 'package:zotikosmanager_ui/logic/models/device.dart';

abstract class ZotikosRepository {
  static Future<List<Device>> getDevicesList() async {
    http.Response response = await http.get("http://127.0.0.1:5000/devices");
    if (response.statusCode == 200) {
      List<Device> devices = jsonDecode(response.body)["devices"]
          .map((json) => Device.fromJson(json))
          .toList()
          .cast<Device>();
      return devices;
    } else {
      return [];
    }
  }
}
