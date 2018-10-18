from flask import current_app
from app import db
from app.models import Apk, Project
import os
from glob import glob
from app.flask_helpers.folder import Folder
from app.flask_helpers.upload import Upload


def folder():
    return Folder(current_app)


def upload_wallpaper(project, request):
    uploading = Upload(current_app)
    wallpaper_folder = folder().create_sub_folder(project, "wallpaper")
    uploaded_file = request.files.getlist("file")
    filename = uploading.upload(destination=wallpaper_folder, ext_conf='IMAGE_EXTENSIONS', files=uploaded_file)
    return filename


def get_wallpaper(project):
    wallpaper_folder = folder().create_sub_folder(project, "wallpaper")
    wallpapers = []
    for wallpaper in glob(wallpaper_folder + '/*'):
        path = "projects/" + project + "/wallpaper/" + os.path.basename(wallpaper)
        wallpapers.append(path)
    return wallpapers


def add_apks(project, request):
    packages = request.form.getlist("apk")
    apks = []
    for package in packages:
        apk = Apk.query.filter_by(package_name=package).first()
        apk.link(project)
        apks.append(apk)
    db.session.commit()
    return packages


def delete_apk(project_id, apk_id):
    project = Project.query.filter_by(id=project_id).first()
    apk = Apk.query.filter_by(id=apk_id).first()
    apk.unlink(project)
    db.session.commit()