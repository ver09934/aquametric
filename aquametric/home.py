from flask import abort, Blueprint, current_app, jsonify, redirect, render_template, request, send_file, url_for
import os
import json

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
    with open(current_app.config["LIVE_CONFIG"], "r") as f:
        live_config = json.load(f)
        req_data = request.get_data(as_text=True)
        return live_config.get(req_data, {"Error": "Sensor ID not found"})

@bp.route('/liveconf-edit', methods=['GET', 'POST'])
def liveconf_edit():
    
    if request.method == 'POST':
        with open(current_app.config["LIVE_CONFIG"], "r") as f:
            live_config = json.load(f)
        
        print(request.form)

        update_conf = {
            request.form['sensor_id']: {
                'update_freq': int(request.form['update_freq']),
                'ota_update': 'ota_update' in request.form
            }
        }

        live_config.update(update_conf)

        with open(current_app.config["LIVE_CONFIG"], "w") as f:
            # json.dump(live_config, f)
            f.write(json.dumps(live_config, indent=4))
        
        with open(current_app.config["LIVE_CONFIG"], "r") as f:
            new_config = json.load(f)
        
        # return 'Config Updated! Check <a href="{url}">{url}</a> to confirm!'.format(url=url_for('home.liveconfig'))
        return 'Config updated to:<pre>{}</pre><a href="{}">Edit Again</a>'.format(json.dumps(new_config, indent=4), url_for('home.liveconf_edit'))
    
    else:
        with open(current_app.config["LIVE_CONFIG"], "r") as f:
            live_config = json.load(f)
            default_key = list(live_config.keys())[0]
            return render_template('liveconf-edit.html', current_conf=live_config, default_key=default_key)

@bp.route('/liveconf-ota', methods=['POST'])
def liveconf_otatoggle():

    with open(current_app.config["LIVE_CONFIG"], "r") as f:
        live_config = json.load(f)
    
    req_data = request.get_data(as_text=True)
    success = True

    def setall(ota_status):
        for sensor_id in live_config.keys():
            live_config[sensor_id]["ota_update"] = ota_status
    
    try:
        req_data = req_data.replace("True", "true").replace("False", "false")
        json_data = json.loads(req_data)
        print("Using JSON...")
        if type(json_data) == bool:
            setall(json_data)
        else:
            for i, (sensor_id, ota_status) in enumerate(json_data.items()):
                print(sensor_id)
                print(ota_status)
                if sensor_id in live_config and type(ota_status) == bool:
                    live_config[sensor_id]["ota_update"] = ota_status
                else:
                    success = False
    except json.decoder.JSONDecodeError:
        print("Using text...")
        req_data = req_data.lower().rstrip()
        if req_data == "true" or req_data == "false":
            ota_status = True if req_data == "true" else False
            setall(ota_status)
        else:
            success = False
        
    with open(current_app.config["LIVE_CONFIG"], "w") as f:
        f.write(json.dumps(live_config, indent=4))

    return jsonify({"Success": success})

@bp.route('/units.json')
def data_units():
    return jsonify(util.data_units)

@bp.route('/favicon.ico')
def favicon():
    return send_file(
        os.path.join(current_app.root_path, 'static/images/favicon.ico'),
        mimetype='image/vnd.microsoft.icon'
    )
