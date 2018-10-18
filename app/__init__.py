from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_navigation import Navigation
from flask_jsglue import JSGlue
from flask_helpers import Device
from config import Config


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
nav = Navigation()
jsglue = JSGlue()
d = Device()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    nav.init_app(app)
    jsglue.init_app(app)
    d.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.device import bp as device_bp
    app.register_blueprint(device_bp, url_prefix='/device')

    from app.project import bp as project_bp
    app.register_blueprint(project_bp, url_prefix='/project')

    from app.apk import bp as apk_bp
    app.register_blueprint(apk_bp, url_prefix='/apk')

    return app


app = create_app()


from app import models
