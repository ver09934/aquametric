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
    from . import data
    app.register_blueprint(home.bp)
    app.register_blueprint(data.bp)

    return app

# TODO: Add current info to side panel
# TODO: Add time last reported to side panel

# TODO: Add data download link
# TODO: Add about page
# TODO: templates in html (reduce code duplication)
# TODO: make sidebar flash actually good
# TODO: Clean up tests

# TODO: Add stage offset stuff to sensors.json
# TODO: Add lots of URL args for graphs
