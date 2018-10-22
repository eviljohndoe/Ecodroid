import unittest
from app import create_app, db
from app.models import DeviceModel as Device, Project, Apk
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class DeviceModalCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_device(self):
        p = Project(name="project1", path="path/project1")
        db.session.add(p)
        db.session.commit()

        d1 = Device(adb_sn="sn_1", constructor="constructeur1", model="model1", imei="imei1", status="Not Configured")
        d2 = Device(adb_sn="sn_2", constructor="constructeur2", model="model2", imei="imei2", status="Not Configured")
        db.session.add(d1)
        db.session.add(d2)
        db.session.commit()

        p.add_device([d1, d2])
        db.session.commit()
        self.assertEqual(p.devices.count(), 2)

        p.delete_device(d2)
        db.session.commit()
        self.assertEqual(p.devices.count(), 1)

    def test_get_project_from_device(self):
        p1 = Project(name="project1", path="path/project1")
        p2 = Project(name="project2", path="path/project2")
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()

        d = Device(adb_sn="sn_1", constructor="constructeur1", model="model1", imei="imei1", status="Not Configured")
        db.session.add(d)
        db.session.commit()

        p1.add_device(d)
        db.session.commit()

        self.assertTrue(d.project().name == "project1")
        self.assertFalse(d.project().name == "project2")

    def test_add_application(self):
        p1 = Project(name="project1", path="path/project1")
        p2 = Project(name="project2", path="path/project2")
        p3 = Project(name="project3", path="path/project3")
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.commit()

        apk1 = Apk(package_name="com.package1", filename="app1.apk",
                   path="folder/app1.apk", version_code="1",
                   version_name="v1")
        apk2 = Apk(package_name="com.package2", filename="app2.apk",
                   path="folder/app2.apk", version_code="1",
                   version_name="v1")
        apk3 = Apk(package_name="com.package3", filename="app3.apk",
                   path="folder/app3.apk", version_code="1",
                   version_name="v1")
        apk4 = Apk(package_name="com.package4", filename="app4.apk",
                   path="folder/app4.apk", version_code="1",
                   version_name="v1")
        db.session.add(apk1)
        db.session.add(apk2)
        db.session.add(apk3)
        db.session.add(apk4)
        db.session.commit()

        apk1.link(p1)
        apk1.link(p2)
        apk2.link(p2)
        apk2.link(p3)
        apk3.link(p1)
        db.session.commit()

        self.assertEqual(p1.apks, [apk1, apk3])
        self.assertEqual(p2.apks, [apk1, apk2])
        self.assertEqual(p3.apks, [apk2])

        self.assertTrue(apk1.is_linked(p1))
        self.assertFalse(apk1.is_linked(p3))


if __name__ == "__main__":
    unittest.main(verbosity=2)
