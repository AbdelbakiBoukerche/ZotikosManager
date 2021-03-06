import socket
from datetime import datetime, timedelta
from time import sleep

from ZotikosManager.controllers.device.device_status import get_device_status
from ZotikosManager.controllers.utils import CORE_LOGGER
from ZotikosManager.models.apis import (
    get_all_device_ids,
    get_device,
    set_device,
    record_device_status,
)

MAX_NOT_HEARD_SECONDS = 90


def calculate_cpu(cpu):
    num_cpus = 0
    cpu_total = 0.0
    for cpu, usage in cpu.items():
        cpu_total += usage["%usage"]
        num_cpus += 1
    return int(cpu_total / num_cpus)


def calculate_memory(memory):
    return int((memory["used_ram"] * 100) / memory["available_ram"])


class DeviceMonitorTask:
    def __init__(self):
        self.terminate = False

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            CORE_LOGGER.info(f"{self.__class__.__name__}: monitor: device terminate pending")

    def monitor(self, interval):

        while True and not self.terminate:
            device_ids = get_all_device_ids()
            CORE_LOGGER.info(f"Device monitor: Beginning device monitoring for {len(device_ids)} devices")

            for device_id in device_ids:
                result, device = get_device(device_id=device_id)

                if result != "Success":
                    CORE_LOGGER.warn(f"Device monitor: Error retrieving device from database. "
                                     f"id: {device_id}, error: {device}")
                    continue

                if device["transport"] == "HTTP-REST":
                    if not device["last_heard"]:
                        continue

                    last_heard_time = datetime.strptime(device["last_heard"], "%Y-%m-%d %H:%M:%S.%F")
                    print(f"Now: {datetime.now()}, last_heard: {last_heard_time}")
                    if (datetime.now() - last_heard_time) > timedelta(seconds=MAX_NOT_HEARD_SECONDS):
                        device["availability"] = False
                        record_device_status(device)
                        set_device(device)
                    continue

                try:
                    ip_address = socket.gethostbyname(device["hostname"])
                    # ip_address = socket.gethostbyaddr(device["ip_address"])
                except (socket.error, socket.gaierror) as e:
                    info = f"Exception Socket error {repr(e)}, continuing to next device"
                    CORE_LOGGER.error(info)
                    ip_address = None

                if self.terminate:
                    break

                CORE_LOGGER.info(f"Device monitor: get environment for {device['name']}")
                device_status = get_device_status(device)

                device["ip_address"] = ip_address
                device["availability"] = device_status["availability"]
                device["response_time"] = device_status["response_time"]
                device["cpu"] = device_status["cpu"]
                device["memory"] = device_status["memory"]

                if device_status["last_heard"]:
                    device["last_heard"] = device_status["last_heard"]

                record_device_status(device)
                set_device(device)
            for _ in range(0, int(interval / 10)):
                sleep(10)
                if self.terminate:
                    break
        CORE_LOGGER.info("Device monitor: Exiting...")
