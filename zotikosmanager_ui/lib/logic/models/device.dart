import 'package:json_annotation/json_annotation.dart';

part 'device.g.dart';

@JsonSerializable()
class Device {
  final int id;
  final String name;
  final String fqdn;
  final String serial;
  // ignore: non_constant_identifier_names
  final String ip_address;
  // ignore: non_constant_identifier_names
  final String mac_address;
  final String vendor;
  final String model;
  final String version;
  final String transport;

  final bool availability;
  // ignore: non_constant_identifier_names
  final int response_time;
  // ignore: non_constant_identifier_names
  final int sla_availability;
  // ignore: non_constant_identifier_names
  final int sla_response_time;

  // ignore: non_constant_identifier_names
  final String last_heard;

  final int cpu;
  final int memory;
  final int uptime;

  // ignore: non_constant_identifier_names
  final bool os_compliance;
  // ignore: non_constant_identifier_names
  final bool config_compliance;
  // ignore: non_constant_identifier_names
  final String last_compliance_check;

  // ignore: non_constant_identifier_names
  final int ssh_port;
  // ignore: non_constant_identifier_names
  final String ncclient_name;
  // ignore: non_constant_identifier_names
  final int netconf_port;

  final String hostname;
  final String username;
  final String password;

  Device({
    this.id,
    this.name,
    this.fqdn,
    this.serial,
    // ignore: non_constant_identifier_names
    this.ip_address,
    // ignore: non_constant_identifier_names
    this.mac_address,
    this.vendor,
    this.model,
    this.version,
    this.transport,
    this.availability,
    // ignore: non_constant_identifier_names
    this.response_time,
    // ignore: non_constant_identifier_names
    this.sla_availability,
    // ignore: non_constant_identifier_names
    this.sla_response_time,
    // ignore: non_constant_identifier_names
    this.last_heard,
    this.cpu,
    this.memory,
    this.uptime,
    // ignore: non_constant_identifier_names
    this.os_compliance,
    // ignore: non_constant_identifier_names
    this.config_compliance,
    // ignore: non_constant_identifier_names
    this.last_compliance_check,
    // ignore: non_constant_identifier_names
    this.ssh_port,
    // ignore: non_constant_identifier_names
    this.ncclient_name,
    // ignore: non_constant_identifier_names
    this.netconf_port,
    this.hostname,
    this.username,
    this.password,
  });

  factory Device.fromJson(Map<String, dynamic> json) => _$DeviceFromJson(json);
  Map<String, dynamic> toJson() => _$DeviceToJson(this);

  @override
  String toString() {
    return "Device: ${this.hostname} -- ${this.ip_address}";
  }
}
