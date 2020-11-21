from ZotikosManager import app
from ZotikosManager.models.apis import (
    get_all_devices
)


@app.route('/devices')
def devices():
    return {
        "device": get_all_devices()
    }
