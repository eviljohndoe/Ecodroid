from flask import jsonify, render_template
from app.device import bp, device
from app.models import DeviceModel, Project


@bp.route('/devices', methods=['GET', 'POST'])
def devices():
    connected = device.get_devices()
    registered = DeviceModel.query.all()
    return render_template('device/devices.html', title='All devices',
                           connected=connected, registered=registered)


# @bp.route('/test_devices', methods=['GET', 'POST'])
# def test_devices():
#     registered = Device.query.all()
#     return jsonify(Device.serialize_list(registered))


@bp.route('/devices/check', methods=['GET', 'POST'])
def check():
    return {}

