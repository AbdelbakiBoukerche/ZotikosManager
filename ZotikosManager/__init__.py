from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cors = CORS(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres:///zotikosmanager'
db = SQLAlchemy(app=app)


import os
interval = os.environ.get("DEVICE_MONITOR_INTERVAL", default='60')
if interval.isnumeric():
    device_monitor_interval = max(10, int(interval))
else:
    device_monitor_interval = 60
interval = os.environ.get("COMPLIANCE_MONITOR_INTERVAL", default='60')
if interval.isnumeric():
    compliance_monitor_interval = max(10, int(interval))
else:
    compliance_monitor_interval = 300
interval = os.environ.get("CONFIGURATION_MONITOR_INTERVAL", default='60')
if interval.isnumeric():
    configuration_monitor_interval = max(10, int(interval))


import ZotikosManager.views.ui_views
from ZotikosManager.models.device import Device
from ZotikosManager.models.device_status import DeviceStatus
from ZotikosManager.models.device_facts import DeviceFacts
from ZotikosManager.models.device_config import DeviceConfig
from ZotikosManager.models.compliance import Compliance

db.create_all()

from ZotikosManager.models.apis import (
    import_devices,
    import_compliance,
    get_all_devices,
    set_facts,
)

import_devices(filename="devices.yaml", filetype="yaml")
import_compliance(filename="compliance.yaml")

DeviceStatus.query.delete()

db.session.commit()


from ZotikosManager.controllers.thread_manager import ThreadManager
ThreadManager.start_device_threads(device_monitor_interval=device_monitor_interval,
                                   compliance_monitor_interval=compliance_monitor_interval,
                                   config_monitor_interval=configuration_monitor_interval)

from ZotikosManager.controllers.utils import CORE_LOGGER


def shutdown():
    CORE_LOGGER.info(f"Entering shutdown sequence...\n\n")

    ThreadManager.initiate_terminate_all_threads()
    ThreadManager.stop_device_threads()

    CORE_LOGGER.info(f"All Threads shutdown, Terminating...\n\n")


import atexit
atexit.register(shutdown)

