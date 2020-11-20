from ZotikosManager import app
from ZotikosManager.controllers.utils import import_devices


@app.route('/devices')
def devices():
    return {
        "device": import_devices()
    }
