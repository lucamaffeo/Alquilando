from flask import Flask, session, render_template, redirect, url_for
from src.core import database, seeds
from src.core.config import config
from src.web.controllers import register_blueprints
from src.web.handlers import error
from src.core.repositories.user import has_permission
import logging 

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])
    database.init_app(app)

    @app.template_filter('merge')
    def _jinja2_merge(dict1, dict2):
        return {**dict1, **dict2}

    @app.context_processor
    def inject_user():
        user_id = session.get('user_id')
        if user_id:
            return {'user_id': user_id}
        return {}

    @app.context_processor
    def inject_has_permission():
        return dict(has_permission=has_permission)

    @app.route("/")
    def home():
        return redirect(url_for("global.inicio_global"))

    register_blueprints(app)

    app.register_error_handler(404, error.error_not_found)
    app.register_error_handler(403, error.forbidden)
    app.register_error_handler(401, error.error_unauthorized)


    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()

    return app
