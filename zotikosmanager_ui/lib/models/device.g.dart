// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'device.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Device _$DeviceFromJson(Map<String, dynamic> json) {
  return Device(
    id: json['id'] as int,
    name: json['name'] as String,
    fqdn: json['fqdn'] as String,
    serial: json['serial'] as String,
    ip_address: json['ip_address'] as String,
    mac_address: json['mac_address'] as String,
    vendor: json['vendor'] as String,
    model: json['model'] as String,
    version: json['version'] as String,
    transport: json['transport'] as String,
    availability: json['availability'] as bool,
    response_time: json['response_time'] as int,
    sla_availability: json['sla_availability'] as int,
    sla_response_time: json['sla_response_time'] as int,
    last_heard: json['last_heard'] as String,
    cpu: json['cpu'] as int,
    memory: json['memory'] as int,
    uptime: json['uptime'] as int,
    os_compliance: json['os_compliance'] as bool,
    config_compliance: json['config_compliance'] as bool,
    last_compliance_check: json['last_compliance_check'] as String,
    ssh_port: json['ssh_port'] as int,
    ncclient_name: json['ncclient_name'] as String,
    netconf_port: json['netconf_port'] as int,
    hostname: json['hostname'] as String,
    username: json['username'] as String,
    password: json['password'] as String,
  );
}

Map<String, dynamic> _$DeviceToJson(Device instance) => <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'fqdn': instance.fqdn,
      'serial': instance.serial,
      'ip_address': instance.ip_address,
      'mac_address': instance.mac_address,
      'vendor': instance.vendor,
      'model': instance.model,
      'version': instance.version,
      'transport': instance.transport,
      'availability': instance.availability,
      'response_time': instance.response_time,
      'sla_availability': instance.sla_availability,
      'sla_response_time': instance.sla_response_time,
      'last_heard': instance.last_heard,
      'cpu': instance.cpu,
      'memory': instance.memory,
      'uptime': instance.uptime,
      'os_compliance': instance.os_compliance,
      'config_compliance': instance.config_compliance,
      'last_compliance_check': instance.last_compliance_check,
      'ssh_port': instance.ssh_port,
      'ncclient_name': instance.ncclient_name,
      'netconf_port': instance.netconf_port,
      'hostname': instance.hostname,
      'username': instance.username,
      'password': instance.password,
    };
