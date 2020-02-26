from flask import Flask
import os

def create_app(test_config=None):

    # instance_relative_config=True will look for config file relative to instance/
    app = Flask(__name__)

    from . import config
    # from . config import Config
    app.config.from_object(config.Config)

    # Create data dir if it does not exist...
    if not os.path.isdir(app.config["DATA_DIR"]):
        os.makedirs(app.config["DATA_DIR"])

    from . import home
    from . import graphs
    app.register_blueprint(home.bp)
    app.register_blueprint(graphs.bp)

    return app
