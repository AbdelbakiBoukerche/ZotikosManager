from ZotikosManager import db


class DeviceConfig(db.Model):

    __tablename__ = "device_config"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    device_id = db.Column(db.Integer)

    timestamp = db.Column(db.Text)
    config = db.Column(db.Text)
    
    def __repr__(self) -> str:
        return f"DeviceConfig {self.device_id}"
