from flask import Blueprint, current_app, redirect, render_template, send_file, url_for
import os

bp = Blueprint('home', __name__)

# TODO: Move sensor sidebar into a separate template which can then be included!
# TODO: Restructure HTMl into templates as well...

@bp.route('/')
def index():
    return render_template('index.html')

'''
@bp.route('/sensor/')
def sensor_redirect():
    return redirect(url_for('sensor_default'))
'''

@bp.route('/sensor/')
@bp.route('/sensor')
def sensor_default():
    return sensor("toaster")
    # TODO: return redirect for url_for(sensor, sensor_id=first_id_in_units_file)

@bp.route('/sensor/<sensor_id>')
def sensor(sensor_id):
    # TODO: Check if sensor ID is valid, if not, throw error
    return render_template('sensor.html', sensor_id=sensor_id)

@bp.route('/sensors.json')
def sensorconfig():
    return send_file(current_app.config["SENSOR_CONFIG"])

@bp.route('/favicon.ico')
def favicon():
    return send_file(
        os.path.join(current_app.root_path, 'static/images/favicon.ico'),
        mimetype='image/vnd.microsoft.icon'
    )
