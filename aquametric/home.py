from flask import Blueprint, current_app, jsonify, render_template, request, send_file
import os
import json

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/sensor')
def sensor():
    return render_template('sensor.html')

@bp.route('/submit', methods=['GET', 'POST'])
def submit():
    content = request.get_json(silent=False)
    with open(os.path.join(os.path.dirname(__file__), "test.txt"), "a") as f:
        f.write(str(content).rstrip())
        f.write("\n")
    return jsonify({"Success": True})

@bp.route('/log')
def log():
    try:
        return send_file(os.path.join(os.path.dirname(__file__), "test.txt"))
    except FileNotFoundError:
        return ("Logfile does not exist.")

@bp.route('/submit-new', methods=['GET', 'POST'])
def submit_new():

    json_data = request.get_json(silent=False)

    try:
        json_data['data'] = json.loads(json_data['data'])
        sensor_id = int(json_data['data']['id'])
    except KeyError:
        return jsonify({"Success": False, "Error": "Missing fields"})
    except ValueError:
        return jsonify({"Success": False, "Error": "Invalid sensor ID"})

    print(json.dumps(json_data, indent=2))

    data_dir = current_app.config["DATA_DIR"]
    data_file = os.path.join(data_dir, "{}.txt".format(sensor_id))

    with open(data_file, "a") as f:
        # f.write(json.dumps(json_data) + "\n")
        json.dump(json_data, f)
        f.write("\n")

    return jsonify({"Success": True})

def json_transform():
    pass

def gen_csv():
    pass

@bp.route('/test')
def test():
    return "Testing!"
