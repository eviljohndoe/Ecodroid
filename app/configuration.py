from app import db, d as Dev
from app.models import DeviceModel


def configure(project, sn):
    #associate_device(project, sn)
    Dev.set_serial(sn=sn)
    #device = Device(app=current_app, sn=_device.adb_sn)
    install_apks(Dev, project.apks)


def associate_device(project, sn):
    project.add_device(sn=sn)
    db.session.commit()


def install_apks(device, apks):
    print 'Install all apks'
    for apk in apks:
        device.installPackage(apk.path)


def square(x):
    # calculate the square of the value of x
    return x*x
