import 'dart:async';

import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:zotikosmanager_ui/logic/models/device.dart';
import 'package:zotikosmanager_ui/repositories/zotikos_repository.dart';

part 'zotikosapi_event.dart';
part 'zotikosapi_state.dart';

class ZotikosApiBloc extends Bloc<ZotikosApiEvent, ZotikosApiState> {
  ZotikosApiBloc() : super(ZotikosApiInitial());

  @override
  Stream<ZotikosApiState> mapEventToState(
    ZotikosApiEvent event,
  ) async* {
    if (event is FetchDevices) {
      try {
        List<Device> devices = await ZotikosRepository.getDevicesList();
        yield FetchingDevicesCompleted(devices);
      } catch (_) {
        yield FetchingDevicesFailed();
      }
    }
  }
}
