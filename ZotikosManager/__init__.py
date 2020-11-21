from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cors = CORS(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres:///zotikosmanager'
db = SQLAlchemy(app=app)

import ZotikosManager.views.ui_views
from ZotikosManager.models.device import Device
from ZotikosManager.models.device_status import DeviceStatus
from ZotikosManager.models.device_facts import DeviceFacts
from ZotikosManager.models.device_config import DeviceConfig
from ZotikosManager.models.compliance import Compliance

db.create_all()

from ZotikosManager.models.apis import (
    import_devices,
    import_compliance
)

import_devices(filename="devices.yaml", filetype="yaml")
import_compliance(filename="compliance.yaml")

DeviceStatus.query.delete()

db.session.commit()


from ZotikosManager.controllers.thread_manager import ThreadManager
ThreadManager.start_device_threads(device_monitor_interval=30, compliance_monitor_interval=30,
                                   config_monitor_interval=30)


def shutdown():
    print(f"\n\n\n-------> Entering shutdown sequence\n\n\n")

    ThreadManager.initiate_terminate_all_threads()
    ThreadManager.stop_device_threads()

    print(f"\n\n\n-------> All Threads shut down, terminating...")


import atexit
atexit.register(shutdown)

# if __name__ == '__main__':
#     app.run()
