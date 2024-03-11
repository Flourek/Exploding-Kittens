from flask import Flask
import logging

from .events import io
from .routes import main 

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "secret"



    app.register_blueprint(main)
    app.allow_unsafe_werkzeug = True
    io.init_app(app)


    # log = logging.getLogger('werkzeug')
    # log.disabled = True

    return app