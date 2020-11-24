//   Widget _buildDeviceListTile({@required Device device}) {
//     return ListTile(
//       leading: device?.availability
//           ? Icon(
//               Icons.check,
//               color: Colors.green,
//             )
//           : Icon(
//               Icons.close,
//               color: Colors.red,
//             ),
//       title: Text("${device.hostname}\n${device.name}"),
//       subtitle: Text("${device.ip_address}"),
//       trailing: IconButton(
//         icon: Icon(Icons.keyboard_arrow_right),
//         tooltip: "Show more information",
//         onPressed: () {},
//       ),
//     );
//   }
// }

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:zotikosmanager_ui/logic/bloc/zotikosapi_bloc.dart';

class DevicesScreen extends StatefulWidget {
  static const String route = "/devices";
  DevicesScreen({Key key}) : super(key: key);

  @override
  _DevicesScreenState createState() => _DevicesScreenState();
}

class _DevicesScreenState extends State<DevicesScreen> {
  ZotikosApiBloc _zotikosApiBloc = ZotikosApiBloc();
  Timer _timer;

  @override
  void initState() {
    _zotikosApiBloc.add(FetchDevices());
    super.initState();
    _timer = Timer.periodic(Duration(seconds: 2), (timer) {
      _zotikosApiBloc.add(FetchDevices());
    });
  }

  @override
  void dispose() {
    _zotikosApiBloc?.close();
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocProvider<ZotikosApiBloc>(
      create: (context) => _zotikosApiBloc,
      child: Scaffold(
        appBar: AppBar(
          title: Text("Devices"),
        ),
        body: BlocBuilder<ZotikosApiBloc, ZotikosApiState>(
          // ignore: missing_return
          builder: (context, state) {
            if (state is ZotikosApiInitial) {
              return Center(
                child: CircularProgressIndicator(),
              );
            }
            if (state is FetchingDevicesFailed) {
              return Center(
                child: Text("Fetching data from API failed"),
              );
            }
            if (state is FetchingDevicesCompleted) {
              print(state.devices.length);
              return Text(state.devices.length.toString());
            }
          },
        ),
      ),
    );
  }
}
