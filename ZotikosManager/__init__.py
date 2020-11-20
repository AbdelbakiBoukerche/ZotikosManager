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

db.create_all()

from ZotikosManager.models.apis import import_devices

import_devices(filename="devices.yaml", filetype="yaml")

db.session.commit()

if __name__ == '__main__':
    app.run()
