from flask import Flask

def create_app(test_config=None):

    app = Flask(__name__)

    from . import home
    from . import test
    
    app.register_blueprint(home.bp)
    app.register_blueprint(test.bp)

    return app
