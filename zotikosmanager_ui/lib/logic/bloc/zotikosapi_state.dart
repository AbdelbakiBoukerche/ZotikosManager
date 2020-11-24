part of 'zotikosapi_bloc.dart';

abstract class ZotikosApiState extends Equatable {
  const ZotikosApiState();

  @override
  List<Object> get props => [];
}

class ZotikosApiInitial extends ZotikosApiState {}

class FetchDevicesCompleted extends ZotikosApiState {
  final List<Device> devices;
  FetchDevicesCompleted(this.devices);

  @override
  List<Object> get props => [devices];
}
