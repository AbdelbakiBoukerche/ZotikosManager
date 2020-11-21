import napalm
from ZotikosManager.models.apis import get_facts, set_facts
from ZotikosManager.controllers.utils import log_console
from ncclient import manager
from xml.dom.minidom import parseString


def get_napalm_device(device):
    if device["os"] == "ios" or device["os"] == "iosxe":
        driver = napalm.get_network_driver("ios")
    elif device["os"] == "nxos-ssh":
        driver = napalm.get_network_driver("nxos_ssh")
    elif device["os"] == "nxos":
        driver = napalm.get_network_driver("nxos")
    else:
        return "Failed", "Unsupported OS"

    if device["os"] in {"ios", "iosxe", "nxos-ssh"}:
        napalm_device = driver(
            hostname=device["hostname"],
            username=device["username"],
            password=device["password"],
            optional_args={"port": device["ssh_port"]},
        )
    else:
        napalm_device = driver(
            hostname=device["hostname"],
            username=device["username"],
            password=device["password"],
        )
    return napalm_device


def get_device_info(device, requested_info, get_live_info=False):
    if device["transport"] == "napalm":
        return get_device_info_napalm(device, requested_info, get_live_info)
    elif device["transport"] == "ncclient":
        return get_device_info_ncclient(device, requested_info, get_live_info)
    elif device["transport"] == "HTTP-REST" and requested_info == "facts":
        facts = {
            "fqdn": device["hostname"],
            "hostname": device["hostname"],
            "os_version": device["version"],
            "serial_number": device["serial"],
            "uptime": device["uptime"],
            "vendor": device["vendor"]
        }
        return 'Success', {"facts": facts}
    else:
        return "Failure", "Unable to retrieve requested info from device"


def get_device_info_napalm(device, requested_info, get_live_info=False):
    if requested_info == "facts" and not get_live_info:
        result, facts = get_facts(device["name"])
        if result == "Success":
            return "Success", {"facts": facts}

    napalm_device = get_napalm_device(device)

    try:
        napalm_device.open()

        if requested_info == "facts":
            facts = napalm_device.get_facts()
            set_facts(device, {"facts": facts})
            # return "success", {"facts": napalm_device.get_facts()}
            return "Success", {"facts": facts}
        elif requested_info == "environment":
            return "Success", {"environment": napalm_device.get_environment()}
        elif requested_info == "interfaces":
            return "Success", {"interfaces": napalm_device.get_interfaces()}
        elif requested_info == "arp":
            return "Success", {"arp": napalm_device.get_arp_table()}
        elif requested_info == "mac":
            return "Success", {"mac": napalm_device.get_mac_address_table()}
        elif requested_info == "config":
            return "Success", {"config": napalm_device.get_config()}
        elif requested_info == "counters":
            return "Success", {"counters": napalm_device.get_interfaces_counters()}

        else:
            return "Failure", "Unknown requested info"
    except BaseException as e:
        log_console(f"Exception in get device info napalm: {repr(e)}")
        return "Failure", repr(e)


def get_device_info_ncclient(device, requested_info, get_live_info=False):
    if requested_info == "facts" and not get_live_info:
        result, facts = get_facts(device["name"])
        if result == "Success":
            return "Success", {"facts": facts}

    nc_conn = manager.connect(
        host=device["hostname"],
        port=device["port"],
        username=device["username"],
        password=device["password"],
        device_params={"name": device["ncclient_name"]},
        hostkey_verify=False,
    )

    config = nc_conn.get_config("running")

    if requested_info == "config":
        return "Success", {"config": {"running": config.xml}}
    elif requested_info == "facts":
        facts = {
            "vendor": device["vendor"],
            "os_version": None,
            "hostname": None,
            "fqdn": None,
            "serial_number": None
        }

        xml_doc = parseString(str(config))

        version = xml_doc.getElementByTagName("version")
        hostname = xml_doc.getElementByTagName("hostname")

        if len(version) > 0:
            facts["os_version"] = version[0].firstChild.nodeValue
        if len(hostname) > 0:
            facts["hostname"] = version[0].firstChild.nodeValue
            facts["fqdn"] = version[0].firstChild.nodeValue

        serial_number = """
                    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
                    <serial/>
                    </System>
                    """

        rsp = nc_conn.get(("subtree", serial_number))
        xml_doc = parseString(str(rsp))

        nc_conn.close_session()
        return "Success", {"facts": facts}

    else:
        if nc_conn:
            nc_conn.close_session()
        return "Failure", "Unsupported requested info"
