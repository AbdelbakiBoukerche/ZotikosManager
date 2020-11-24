part of 'zotikosapi_bloc.dart';

abstract class ZotikosApiState extends Equatable {
  const ZotikosApiState();

  @override
  List<Object> get props => [];
}

class ZotikosApiInitial extends ZotikosApiState {}

class FetchingDevicesFailed extends ZotikosApiState {}

class FetchingDevicesCompleted extends ZotikosApiState {
  final List<Device> devices;
  FetchingDevicesCompleted(this.devices);

  @override
  List<Object> get props => [devices];
}
