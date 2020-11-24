from datetime import datetime
import time

from ZotikosManager.controllers.device.device_info import get_device_info
from ZotikosManager.controllers.utils import CORE_LOGGER


def calculate_cpu(cpu):
    num_cpus = 0
    cpu_total = 0.0
    for cpu, usage in cpu.items():
        cpu_total += usage["%usage"]
        num_cpus += 1
    return int(cpu_total / num_cpus)


def calculate_memory(memory):
    return int((memory["used_ram"] * 100) / memory["available_ram"])


def get_device_status(device):
    device_status = dict()
    device_status["availability"] = False
    device_status["response_time"] = None
    device_status["cpu"] = None
    device_status["memory"] = None
    device_status["last_heard"] = None

    env = None
    response_time = None

    if device["os"] in {"ios", "iosxe", "nxos-ssh"} and device["transport"] == "napalm":
        try:
            time_start = time.time()
            result, env = get_device_info(device, "environment")
            response_time = time.time() - time_start
        except BaseException as e:
            info = f"Exception in monitoring device, get environment: {repr(e)}"
            CORE_LOGGER.error(info)
            result = "Failed"

    else:
        try:
            time_start = time.time()
            result, fact = get_device_info(device, "facts", get_live_info=True)
            response_time = time.time() - time_start
        except BaseException as e:
            info = f"Exception in monitoring device, get facts: {repr(e)}"
            CORE_LOGGER.error(info)
            result = "Failed"

    if result != "Success":
        CORE_LOGGER.warn(f"Availability failed for device: {device['name']}")

    else:
        CORE_LOGGER.info(f"Availability succeeded for device: {device['name']}")
        device_status["availability"] = True
        if response_time:
            device_status["response_time"] = int(response_time * 1000)
        device_status["last_heard"] = str(datetime.now())[:-3]

        if env:
            device_status["cpu"] = calculate_cpu(env["environment"]["cpu"])
            device_status["memory"] = calculate_memory(env["environment"]["memory"])

    return device_status
