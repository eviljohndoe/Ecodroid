from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from app import db, d as Device
from app.project import bp, _project
from app.project._project import folder
from app.device import device
from app.models import Project, Apk
from app.configuration import configure as conf, square, install_apks
from app.project.forms import ProjectForm, EditProjectForm
from multiprocessing import Pool, Process
import threading


@bp.route('/projects', methods=["GET", "POST"])
def projects():
    form = ProjectForm()
    projects = Project.query.all()
    if form.validate_on_submit():
        path = folder().create_folder(form.name.data.lower())
        project = Project(name=form.name.data.lower(), path=path)
        db.session.add(project)
        db.session.commit()
        flash("{} has been created".format(form.name.data.upper()))
        return redirect(url_for("project.projects"))
    return render_template('project/projects.html', title='All projects', form=form, projects=projects)


@bp.route('/<id>', methods=["GET", "POST"])
def project(id):
    project = Project.query.filter_by(id=id).first()
    connected = device.get_devices()
    all_apks = Apk.query.all()
    not_linked_apks = project.get_apks_not_link()
    linked_apks = project.apks
    wallpapers = _project.get_wallpaper(project.name.lower())

    # if request.method == 'POST':
    #     f = request.form.get("form_id", "")
    #     if f == "applications":
    #         _project.add_apks(project=project, request=request)
    #     if f == "wallpaper":
    #         _project.upload_wallpaper(request=request, project=project.name.lower())
    #     return redirect(url_for("project.project", id=id))

    return render_template('project/project.html', title=project.name.upper(), project=project,
                           connected=connected, apks=linked_apks, not_linked_apks=not_linked_apks,
                           all_apks=all_apks, wallpapers=wallpapers)


@bp.route('/upload/<id>', methods=["POST"])
def upload(id):
    project = Project.query.filter_by(id=id).first()
    filename = _project.upload_wallpaper(request=request, project=project.name.lower())
    path = []
    for f in filename:
        path.append("projects/" + project.name.lower() + "/wallpaper/" + f)

    return jsonify(path)


@bp.route('/add_apk/<id>', methods=["POST"])
def add_apk(id):
    project = Project.query.filter_by(id=id).first()
    apks = _project.add_apks(project=project, request=request)
    return jsonify(apks)


@bp.route('/delete/<id>', methods=["GET", "POST"])
def delete(id):
    project = Project.query.filter_by(id=id).first()
    if project.has_devices():
        flash("{} has devices".format(project.name))
        return redirect(url_for("project.projects"))
    db.session.delete(project)
    db.session.commit()
    folder().remove_project(project.name.lower())
    flash("{} has been deleted".format(project.name.upper()))
    return redirect(url_for("project.projects"))


@bp.route('/delete_apk/<apk_id>/<project_id>', methods=["GET", "POST"])
def delete_apk(apk_id, project_id):
    _project.delete_apk(apk_id=apk_id, project_id=project_id)
    return redirect(url_for("project.project", id=project_id))


@bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    project = Project.query.filter_by(id=id).first()
    form = EditProjectForm(project.name)
    if form.validate_on_submit():
        old_name = project.name
        project.name = form.name.data.lower()
        new_path = folder().rename_project(old_name.lower(), form.name.data.lower())
        project.path = new_path
        db.session.commit()
        flash("The project {} has been changed to {}".format(old_name.upper(), form.name.data.upper()))
        return jsonify(status='ok')
    return render_template('project/edit/edit.html', form=form, project=project)


@bp.route('/configure/<id>', methods=['GET', 'POST'])
def configure(id):
    connected = device.get_devices()
    project = Project.query.filter_by(id=id).first()
    if connected:
        # p = None
        # for d in connected:
        #     p = Process(target=conf(project=project, _device=d))
        # p.start()
        for d in connected:
            sn = d.adb_sn
            Device.set_serial(sn)
            print("configure {}".format(sn))
            threading.Thread(target=install_apks, args=(Device, project.apks,)).start()
            #conf(project=project, sn=sn)

    return redirect(url_for("project.project", id=id))
