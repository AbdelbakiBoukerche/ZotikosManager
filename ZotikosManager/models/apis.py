import yaml
import json
from ZotikosManager import db
from ZotikosManager.models.device import Device


def set_device(devices):
    ids = set()
    names = set()

    for device in devices:
        if device["id"] in ids:
            # TODO log event
            continue
        if device["name"] in names:
            # TODO log event
            continue

        ids.add(device["id"])
        names.add(device["name"])

        device_instance = Device(**device)
        db.session.add(device_instance)

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

    set_device(devices)
    return {
        "devices": devices
    }
