import logging.config

import os
from flask import Flask, Blueprint
from MoistureReadingsFrontEnd import settings
from MoistureReadingsFrontEnd.api.moisture.endpoints.moisture_readings import ns as moisture_readings_namespace
from MoistureReadingsFrontEnd.api.restplus import api
from MoistureReadingsFrontEnd.database import db
from MoistureReadingsFrontEnd.database import reset_database
from MoistureReadingsFrontEnd.web import web

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app):
    #flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.secret_key = settings.FLASK_SECRET_KEY

def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')

    api.init_app(blueprint)
    api.add_namespace(moisture_readings_namespace)
    flask_app.register_blueprint(blueprint)

    flask_app.register_blueprint(web.web_blueprint)

    db.init_app(flask_app)


def main():
    initialize_app(app)
    # uncomment this to reset the dabase.
    if os.environ.get('RESET_DATABASE') == 'TRUE':
        log.info('RESETTING DATABASE')
        with app.app_context():
            reset_database()

    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG, host='0.0.0.0')


if __name__ == "__main__":
    main()
