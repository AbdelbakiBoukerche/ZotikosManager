from ZotikosManager import app
from flask import request
from ZotikosManager.controllers.device.device_info import get_device_info
from ZotikosManager.models.apis import (
    get_all_devices,
    get_device,
)


@app.route('/devices')
def devices():
    return {
        "devices": get_all_devices()
    }


@app.route('/device', methods=["GET"])
def device_info():
    if request.method == "GET":

        device_name = request.args.get("device")
        requested_info = request.args.get("info")
        live = request.args.get("live")

        if not device_name or not requested_info:
            return "Must provide device and info", 400

        result, info = get_device(device_name=device_name)
        if result == "Failed":
            return info, 406
        device = info

        if not live:
            get_live_info = False
        else:
            if live.lower() not in {"true", "false"}:
                return "Value of 'live', if specified, must be either 'true' or 'false'"
            else:
                get_live_info = bool(live)

        status, result_info = get_device_info(device, requested_info, get_live_info)
        if status == "Success":
            return result_info, 200
        else:
            return result_info, 406
