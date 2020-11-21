from datetime import datetime
from time import sleep

from ZotikosManager.controllers.device.config_diff import config_diff
from ZotikosManager.controllers.device.device_info import get_device_info
from ZotikosManager.controllers.utils import log_console
from ZotikosManager.models.compliance import Compliance
from ZotikosManager.models.apis import (
    get_all_device_ids,
    get_device,
    set_device
)


def check_version(device, standard, actual):
    if device["vendor"] == "cisco" and device["os"] == "iosxe":
        version_parts = actual.split(",")
        if len(version_parts) == 3 and version_parts[1].find(standard) >= 0:
            return True

    if actual.find(standard) >= 0:
        return True

    return False


def check_os_compliance(device):
    facts = None
    standard = Compliance.query.filter_by(**{"vendor": device["vendor"], "os": device["os"]}).one_or_none()
    if standard is None:
        log_console(f"Error retrieving compliance record for this device: {device['name']}")
        return False

    try:
        result, facts = get_device_info(device, "facts", get_live_info=True)
    except BaseException as e:
        log_console(f"Exception getting device info in compliance monitoring for device: {device['name']}: {repr(e)}")
        result = "Failed"

    if result == "Failed" or not facts or 'facts' not in facts or "os_version" not in facts["facts"]:
        log_console(f"Error retrieving version info for device: {device['name']}")
        return False

    return check_version(device, standard=standard.standard_version, actual=facts["facts"]["os_version"])


def check_config_compliance(device):
    standard = Compliance.query.filter_by(**{"vendor": device["vendor"], "os": device["os"]}).one_or_none()
    if standard is None:
        log_console(f"Error retrieving compliance record for device: {device['name']}")
        return False

    standard_filename = "ZotikosManager/data/" + standard.standard_config_file
    print(f"Standard file: {standard_filename}")
    result, diff = config_diff(device, standard_filename)

    if result != "Success":
        return False
    if len(diff) > 0:
        with open(standard_filename + ".diff" + device["name"], "w") as config_out:
            config_out.write(diff)
        return False
    return True


class ComplianceMonitorTask:
    def __init__(self):
        self.terminate = False

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            log_console(f"{self.__class__.__name__}: monitor: compliance terminate pending")

    def monitor(self, interval):

        while True and not self.terminate:
            device_ids = get_all_device_ids()
            log_console(f"Monitor: Beginning compliance monitoring for {len(device_ids)} devices")

            for device_id in device_ids:
                if self.terminate:
                    break

                result, device = get_device(device_id=device_id)

                if result != "Success":
                    log_console(f"Compliance monitor: Error Retrieving device from database. id: {device_id},"
                                "error: {device}")
                    continue

                if device["availability"]:
                    device["os_compliance"] = check_os_compliance(device)
                    device["config_compliance"] = check_config_compliance(device)
                    device["last_compliance_check"] = str(datetime.now())[:-3]

                set_device(device)
            for _ in range(0, int(interval / 10)):
                sleep(10)
                if self.terminate:
                    break
        log_console(f"...Exiting monitor:compliance")
