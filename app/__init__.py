from flask import Flask
from flask_socketio import SocketIO
import os

socketio = SocketIO()

def create_app(debug=False):
    """Create an aplication."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'dev'
    app.config['DATABASE'] = os.path.join(app.instance_path, 'app.sqlite')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from . import db
    db.init_app(app)
    socketio.init_app(app)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    return app
