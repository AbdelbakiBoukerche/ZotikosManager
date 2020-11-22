from time import sleep

from ZotikosManager.controllers.utils import CORE_LOGGER
from ZotikosManager.controllers.device.device_info import get_device_info
from ZotikosManager.models.apis import (
    get_all_device_ids,
    get_device,
    record_device_config,
)


class ConfigurationMonitorTask:
    def __init__(self):
        self.terminate = False

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            CORE_LOGGER.info(f"{self.__class__.__name__}: monitor: configuration terminate pending.")

    def monitor(self, interval):
        while True and not self.terminate:

            device_ids = get_all_device_ids()
            CORE_LOGGER.info(f"Configuration monitor: Beginning configuration monitoring for "
                             f"{len(device_ids)} devices")

            for device_id in device_ids:
                if self.terminate:
                    break

                result, device = get_device(device_id=device_id)

                if result != "Success":
                    CORE_LOGGER.warn(f"Configuration monitor: Error retrieving device from database. "
                                     f"id: {device_id}, error: {device}")
                    continue

                try:
                    result, config = get_device_info(device, "config", get_live_info=True)
                    if result != "Success":
                        CORE_LOGGER.warn(f"Unable to get device info (config) for {device['name']}")
                        continue
                except BaseException as e:
                    CORE_LOGGER.error(f"Exception getting device info in configuration monitoring for"
                                      f"{device['name']}: {repr(e)}")
                    continue

                record_device_config(device_id, config["config"]["running"])

            for _ in range(0, int(interval / 10)):
                sleep(10)
                if self.terminate:
                    break
        CORE_LOGGER.info("Configuration monitor: Exiting...")
