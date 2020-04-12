from flask import abort, Blueprint, current_app, jsonify, redirect, render_template, request, send_file, url_for
import os

from . import util

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    return render_template('index.html', data_units=util.data_units)

@bp.route('/sensor/<sensor_id>')
def sensor(sensor_id):
    
    sensor_config = current_app.config["SENSOR_CONFIG"]
    data_dir = current_app.config["DATA_DIR"]
    logfile = util.get_logfile_path(data_dir, sensor_id)

    if sensor_id not in util.get_sensor_list(sensor_config):
        abort(500, "Sensor ID is not in the sensor list.")
    if not os.path.isfile(logfile):
        abort(500, "No data exists for the sensor.")

    sensor_info = util.get_sensor_info(sensor_id, sensor_config)

    passthrough_args = ["hours"]
    img_args = {key: value for key, value in request.args.items() if key in passthrough_args}

    return render_template(
        'sensor.html',
        data_units=util.data_units,
        sensor_info=sensor_info,
        sensor_id=sensor_id,
        current_data=util.get_json(logfile, latest=True),
        img_args=img_args
    )

@bp.route('/sensors.json')
def sensorconfig():
    return send_file(current_app.config["SENSOR_CONFIG"])

@bp.route('/liveconf.json')
def liveconfig():
    return send_file(current_app.config["LIVE_CONFIG"])

@bp.route('/test', methods=['POST'])
def test():
    import json
    with open(current_app.config["LIVE_CONFIG"], "r") as f:
        live_config = json.load(f)
        req_data = request.get_data(as_text=True)
        return live_config.get(req_data, {"Error": "Sensor ID not found"})

@bp.route('/units.json')
def data_units():
    return jsonify(util.data_units)

@bp.route('/favicon.ico')
def favicon():
    return send_file(
        os.path.join(current_app.root_path, 'static/images/favicon.ico'),
        mimetype='image/vnd.microsoft.icon'
    )
