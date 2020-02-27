from flask import Blueprint, current_app, render_template, send_file
import os

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/sensor')
def sensor():
    return render_template('sensor.html')

@bp.route('/sensors.json')
def sensorconfig():
    return send_file(current_app.config["SENSOR_CONFIG"])

@bp.route('/favicon.ico')
def favicon():
    return send_file(
        os.path.join(current_app.root_path, 'static/images/favicon.ico'),
        mimetype='image/vnd.microsoft.icon'
    )
