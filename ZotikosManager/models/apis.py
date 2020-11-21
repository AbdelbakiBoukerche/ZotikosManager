import yaml
import json
from sqlalchemy import desc, or_, func
from datetime import datetime
from ZotikosManager import db
from ZotikosManager.models.device import Device
from ZotikosManager.models.device_facts import DeviceFacts
from ZotikosManager.models.device_status import DeviceStatus
from ZotikosManager.models.device_config import DeviceConfig
from ZotikosManager.models.compliance import Compliance
from ZotikosManager.models.utils import get_model_as_dict
from ZotikosManager.controllers.utils import log_console


def get_device(device_id=None, device_name=None):
    if device_id and device_name:
        return "Failed", "Must provide either 'device_id' or 'device_name', but not both."

    if device_id:
        search = {"id": device_id}
    elif device_name:
        search = {"name": device_name}
    else:
        return "Failed", "Must provide either 'device_id' or 'device_name'"

    device_instance = db.session.query(Device).filter_by(**search).one_or_none()
    if not device_instance:
        return "Failed", "Could not find device in database"

    return "Success", get_model_as_dict(device_instance)


def get_all_devices():
    device_instances = db.session.query(Device).all()

    devices = list()
    for device_instance in device_instances:
        devices.append(get_model_as_dict(device_instance))

    return devices


def get_all_device_ids():
    device_ids = db.session.query(Device.id).all()
    return [
        device_id for device_id in device_ids
    ]


def get_facts(device_name):
    facts_instance = (
        db.session.query(DeviceFacts).filter_by(**{"device_name": device_name}).one_or_none()
    )
    
    if not facts_instance:
        return "Failed", "Could not find device facts in database"
    
    return "Success", get_model_as_dict(facts_instance)


def set_devices(devices):
    ids = set()
    names = set()

    for device in devices:
        if device["id"] in ids:
            log_console("Error: Duplicate device id")
            continue
        if device["name"] in names:
            log_console("Error: Duplicate device name")
            continue

        ids.add(device["id"])
        names.add(device["name"])

        device_instance = Device(**device)
        db.session.add(device_instance)

    db.session.commit()


def set_device(device):
    search = {"name": device["name"]}
    device_instance = db.session.query(Device).filter_by(**search).one_or_none()
    if not device_instance:
        device_instance = Device(**device)
        db.session.add(device_instance)
    else:
        if "ip_address" in device and device["ip_address"]:
            device_instance.ip_address = device["ip_address"]
        if "serial" in device and device["serial"]:
            device_instance.serial = device["serial"]
        if "mac_address" in device and device["mac_address"]:
            device_instance.mac_address = device["mac_address"]
        if "vendor" in device and device["vendor"]:
            device_instance.vendor = device["vendor"]
        if "os" in device and device["os"]:
            device_instance.os = device["os"]
        if "version" in device and device["version"]:
            device_instance.version = device["version"]
        if "model" in device and device["model"]:
            device_instance.model = device["model"]
        if "fqdn" in device and device["fqdn"]:
            device_instance.fqdn = device["fqdn"]
        if "uptime" in device and device["uptime"]:
            device_instance.uptime = device["uptime"]
        if "availability" in device and device["availability"] is not None:
            device_instance.availability = device["availability"]
        if "response_time" in device and device["response_time"]:
            device_instance.response_time = device["response_time"]
        if "last_heard" in device and device["last_heard"]:
            device_instance.last_heard = device["last_heard"]
        if "cpu" in device and device["cpu"]:
            device_instance.cpu = device["cpu"]
        if "memory" in device and device["memory"]:
            device_instance.memory = device["memory"]
        if "os_compliance" in device and device["os_compliance"] is not None:
            device_instance.os_compliance = device["os_compliance"]
        if "config_compliance" in device and device["config_compliance"] is not None:
            device_instance.config_compliance = device["config_compliance"]
        if "last_compliance_check" in device and device["last_compliance_check"]:
            device_instance.last_compliance_check = device["last_compliance_check"]

    db.session.commit()


def set_facts(device, facts):

    device_facts = dict()
    device_facts["fqdn"] = facts["facts"]["fqdn"]
    device_facts["uptime"] = facts["facts"]["uptime"]
    device_facts["vendor"] = facts["facts"]["vendor"]
    device_facts["os_version"] = facts["facts"]["os_version"]
    device_facts["serial_number"] = facts["facts"]["serial_number"]
    device_facts["model"] = facts["facts"]["model"]
    device_facts["hostname"] = facts["facts"]["hostname"]

    device_facts["device_name"] = device["name"]
    device_facts_instance = DeviceFacts(**device_facts)

    facts_instance = (
        db.session.query(DeviceFacts).filter_by(**{"device_name": device_facts["device_name"]}).one_or_none()
    )

    if not facts_instance:
        db.session.add(device_facts_instance)

    else:
        facts_instance.fqdn = device_facts["fqdn"]
        facts_instance.uptime = device_facts["uptime"]
        facts_instance.vendor = device_facts["vendor"]
        facts_instance.os_version = device_facts["os_version"]
        facts_instance.serial_number = device_facts["serial_number"]
        facts_instance.model = device_facts["model"]
        facts_instance.hostname = device_facts["hostname"]
        facts_instance.device_name =device_facts["device_name"]

    db.session.commit()


def import_devices(filename=None, filetype=None):
    if not filename or not filetype:
        return None

    db.session.query(Device).delete()
    with open("ZotikosManager/data/" + filename, "r") as import_file:
        if filetype.lower() == "json":
            devices = json.load(import_file.read())
        elif filetype.lower() == "yaml":
            devices = yaml.safe_load(import_file.read())
        else:
            return None

    set_devices(devices)
    return {
        "devices": devices
    }


def export_devices(filename=None, filetype=None):
    if not filename or not filetype:
        return None

    devices = get_all_devices()

    with open(filename, "w") as output_file:
        if filetype.lower() == "json":
            output_file.write(json.dumps(devices))
        elif filetype.lower() == "yaml":
            output_file.write(yaml.dump(devices))
        else:
            return None


def import_compliance(filename=None):
    db.session.query(Compliance).delete()

    try:
        with open("ZotikosManager/data/" + filename, "r") as import_file:
            standards = yaml.safe_load(import_file.read())
    except FileNotFoundError as e:
        print(f"Error: {e}")

    for standard in standards:
        standard_instance = Compliance(**standard)
        db.session.add(standard_instance)

    db.session.commit()
    return


def record_device_status(device):
    device_status = dict()

    device_status["device_id"] = device["id"]
    device_status["timestamp"] = str(datetime.now())[:-3]
    device_status["availability"] = device["availability"]
    device_status["response_time"] = device["response_time"]
    device_status["cpu"] = device["cpu"]
    device_status["memory"] = device["memory"]

    device_status_instance = DeviceStatus(**device_status)
    db.session.add(device_status_instance)

    db.session.commit()


def get_device_status_data(device_name, num_datapoints):
    result, info = get_device(device_name=device_name)
    if result != "Success":
        return result, info

    device_id = info["id"]
    device_status_instances = (
        db.session.query(DeviceStatus)
        .fitler_by(**{"device_id": device_id})
        .order_by(desc(DeviceStatus.timestamp))
        .limit(num_datapoints)
        .all()
    )

    device_status_data = list()
    for device_status_instance in device_status_instances:
        device_status_data.append(get_model_as_dict(device_status_instance))

    return device_status_data


def record_device_config(device_id, config):
    device_config = dict()
    device_config["device_id"] = device_id
    device_config["timestamp"] = str(datetime.now())[:-3]
    device_config["config"] = config

    device_config_instance = DeviceConfig(**device_config)
    db.session.add(device_config_instance)

    db.session.commit()


def get_device_config_diff(device, num_configs):
    device_configs = (
        db.session.query(DeviceConfig)
        .filter_by(**{"device_id": device["id"]})
        .order_by(desc(DeviceConfig.timestamp))
        .limit(num_configs)
        .all()
    )

    config_diff = {"current": dict(), "old": dict()}
    if len(device_configs) == 0:
        return "Success", config_diff

    config_diff["current"]["timestamp"] = device_configs[0].timestamp
    config_diff["current"]["config"] = device_configs[0].config

    for device_config in device_configs:
        config_diff["old"]["timestamp"] = device_config.timestamp
        config_diff["old"]["config"] = device_config.config

        if config_diff["current"]["config"] != device_config.config:
            return "Success", config_diff
    else:
        return "Success", config_diff
