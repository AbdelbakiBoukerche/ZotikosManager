from ZotikosManager.controllers.utils import log_console
from ZotikosManager.controllers.device.device_info import get_napalm_device


def config_diff(device, config_to_diff):
    if device["transport"] == "napalm":
        napalm_device = get_napalm_device(device)

        try:
            napalm_device.open()

            napalm_device.load_merge_candidate(filename=config_to_diff)
            return "Success", napalm_device.commit_config()
        except BaseException as e:
            log_console(f"Exception in doing load_merge_candidate: {repr(e)}")
            return "Failure", repr(e)
    else:
        log_console(f"Unable to compare configuration, no live config to compare")
        return "Failure", "Unable to compare configurations"
