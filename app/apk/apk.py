import os
from flask import current_app
from app import db
from app.models import Apk
from app.flask_helpers.folder import Folder
from app.flask_helpers.upload import Upload
from app.flask_helpers.apk_parse.apk import APK


def folder():
    return Folder(current_app)


def upload(request):
    uploading = Upload(current_app)
    apk_folder = folder().create_folder("apks")
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filename = uploading.upload(destination=apk_folder, ext_conf='APP_EXTENSIONS', files=uploaded_files)
    if type(filename) is list:
        apks = []
        for file in filename:
            apk = os.path.join(apk_folder, file)
            apks.append(apk)
        save(apks)
    else:
        apks = os.path.join(apk_folder, filename)
        save(apks)
    return filename


def save(apks):
    if type(apks) is list:
        for apk in apks:
            apkf = APK(apk)
            a = Apk(
                package_name=apkf.get_package(),
                filename=os.path.basename(apkf.get_filename()),
                path=apkf.get_filename(),
                version_code=apkf.get_androidversion_code(),
                version_name=apkf.get_androidversion_name()
            )
            db.session.add(a)
        db.session.commit()
    else:
        apkf = APK(apks)
        a = Apk(
            package_name=apkf.get_package(),
            filename=os.path.basename(apkf.get_filename()),
            path=apkf.get_filename(),
            version_code=apkf.get_androidversion_code(),
            version_name=apkf.get_androidversion_name()
        )
        db.session.add(a)
        db.session.commit()


def delete(apk):
    folder().remove(apk.path)
    db.session.delete(apk)
    db.session.commit()

