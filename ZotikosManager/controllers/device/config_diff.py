from ZotikosManager.controllers.utils import CORE_LOGGER
from ZotikosManager.controllers.device.device_info import get_napalm_device


def config_diff(device, config_to_diff):
    if device["transport"] == "napalm":
        napalm_device = get_napalm_device(device)

        try:
            napalm_device.open()

            napalm_device.load_merge_candidate(filename=config_to_diff)
            return "Success", napalm_device.commit_config()
        except BaseException as e:
            CORE_LOGGER.error(f"Exception in doing load_merge_candidate: {repr(e)}")
            return "Failure", repr(e)
    else:
        CORE_LOGGER.error(f"Unable to compare configurations. No live config to compare")
        return "Failure", "Unable to compare configurations"
