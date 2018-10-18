from flask import render_template
from app import nav
from app.main import bp

nav.Bar('top', [
    nav.Item('Dashboard', 'main.index'),
    nav.Item('Project', 'project.projects'),
    nav.Item('Device', 'device.devices'),
    nav.Item('Applications', 'apk.applications'),
    nav.Item('About', 'main.about')
])


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')


@bp.route('/about')
def about():
    return render_template('about.html', title='About')
