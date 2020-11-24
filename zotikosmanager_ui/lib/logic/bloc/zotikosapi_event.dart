part of 'zotikosapi_bloc.dart';

abstract class ZotikosApiEvent extends Equatable {
  const ZotikosApiEvent();

  @override
  List<Object> get props => [];
}

class FetchDevices extends ZotikosApiEvent {}
