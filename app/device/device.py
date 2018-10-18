from flask import current_app
#from app.flask_helpers import Device as Dev
from app import db, d as Dev
from app.models import DeviceModel


def get_devices():
    plugged_in = detect()
    connected = []
    if plugged_in:
        for device in plugged_in:
            connected.append(DeviceModel.query.filter_by(adb_sn=device).first())
        return connected
    return None


def detect():
    # device = Dev(app=current_app)
    devices = Dev.detect()
    devices = devices.split()
    save(devices)
    return devices


def save(devices):
    if devices:
        for sn in devices:
            Dev.set_serial(sn=sn)
            constructor = Dev.shell("getprop ro.product.manufacturer")
            model = Dev.shell("getprop ro.product.model")
            imei = Dev.getIMEI()
            if "EADEAE2000EADEAE" in imei:
                imei = Dev.shell("getprop ril.serialnumber")
            if exists(sn):
                print("already added")
            else:
                print("saving in database")
                de = DeviceModel(adb_sn=sn, constructor=constructor, model=model, imei=imei, status="Not Configured")
                db.session.add(de)
        db.session.commit()


def exists(sn):
    return DeviceModel.query.filter_by(adb_sn=sn).first()


