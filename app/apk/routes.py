from flask import render_template, request, redirect, url_for, jsonify
from app.apk import bp, apk
from app.models import Apk


@bp.route('/applications', methods=['GET', 'POST'])
def applications():
    print(request.path)
    apks = Apk.query.all()
    return render_template('apk/apks.html', title='Applications', apks=apks)


@bp.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    app = Apk.query.filter_by(id=id).first()
    apk.delete(app)
    return redirect(url_for("apk.applications"))


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    filename = apk.upload(request)
    return jsonify(filename)