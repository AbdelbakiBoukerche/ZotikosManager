from ZotikosManager import db


class DeviceStatus(db.Model):

    __tablename__ = "device_status"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    device_id = db.Column(db.Integer)

    timestamp = db.Column(db.Text)
    availability = db.Column(db.Boolean)
    response_time = db.Column(db.Integer)
    cpu = db.Column(db.Integer)
    memory = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f"DeviceStatus {self.device_id}"
