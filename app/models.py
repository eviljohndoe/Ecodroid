from sqlalchemy.inspection import inspect
from datetime import datetime
from app import db


class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


project_apks = db.Table(
    'projects_apks',
    db.Column("apk_id", db.Integer, db.ForeignKey('apk.id')),
    db.Column("project_id", db.Integer, db.ForeignKey('project.id'))
)


class Project(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    path = db.Column(db.String(256))
    devices = db.relationship('DeviceModel', backref='list', lazy='dynamic')
    apks = db.relationship(
        'Apk', secondary=project_apks,
        backref=db.backref('projects', lazy='dynamic')
    )

    def __repr__(self):
        return '<Project {}>'.format(self.name)

    def serialize(self):
        d = Serializer.serialize(self)
        return d

    def add_device(self, device=None, sn=None):
        if device is not None:
            if type(device) is list:
                for d in device:
                    if self.check_device(d) is None:
                        self.devices.append(d)
            else:
                if self.check_device(device) is None:
                    self.devices.append(device)
        if sn is not None:
            device = DeviceModel.query.filter_by(adb_sn=sn).first()
            if self.check_device(device) is None:
                self.devices.append(device)

    def delete_device(self, device):
        if type(device) is list:
            for d in device:
                if self.check_device(d):
                    if self.id == self.check_device(d).id:
                        self.devices.remove(d)
        else:
            if self.check_device(device):
                if self.id == self.check_device(device).id:
                    self.devices.remove(device)

    def check_device(self, device):
        return device.project()

    def has_devices(self):
        if self.devices.count() > 0:
            return True
        return False

    def get_apks_not_link(self):
        not_linked = []
        all_apks = Apk.query.all()
        for apk in all_apks:
            if not apk.is_linked(self):
                not_linked.append(apk)
        return not_linked


class DeviceModel(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    adb_sn = db.Column(db.String(128), index=True, unique=True)
    constructor = db.Column(db.String(64))
    model = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    imei = db.Column(db.String(128), index=True, unique=True)
    status = db.Column(db.String(128), default="not configured")
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return '<Device {}>'.format(self.adb_sn)

    def serialize(self):
        d = Serializer.serialize(self)
        return d

    def project(self, serialize=False):
        project = Project.query.filter_by(id=self.project_id).first()
        if serialize:
            return project.serialize()
        return project


class Apk(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    package_name = db.Column(db.String(128), index=True, unique=True)
    filename = db.Column(db.String(128))
    path = db.Column(db.String(256))
    version_code = db.Column(db.String(64))
    version_name = db.Column(db.String(64))

    def __repr__(self):
        return '<Apk {}>'.format(self.package_name)

    def link(self, project):
        if type(project) is list:
            for p in project:
                if not self.is_linked(project):
                    self.projects.append(p)
                else:
                    print("{} is already linked".format(project.name))
        else:
            if not self.is_linked(project):
                self.projects.append(project)
            else:
                print("{} is already linked".format(project.name))

    def unlink(self, project):
        if type(project) is list:
            for p in project:
                if self.is_linked(project):
                    self.projects.remove(p)
                else:
                    print("{} is not linked".format(project.name))
        else:
            if self.is_linked(project):
                self.projects.remove(project)
            else:
                print("{} is not linked".format(project.name))

    def is_linked(self, project):
        return Apk.query.filter(Apk.projects.any(id=project.id)).filter_by(id=self.id).count() > 0
