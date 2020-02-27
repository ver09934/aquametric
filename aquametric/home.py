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

    # NOTE: May want to remove conversion of sensor ID to int, allowing for
    # sensor ID strings which are not strings which can be converted to integers.
    # Would be able to remove ValueError handling if we did this.

    try:
        json_data['data'] = json.loads(json_data['data'])
        sensor_id = int(json_data['data']['id'])
    except KeyError:
        return jsonify({"Success": False, "Error": "Missing fields"})
    except ValueError:
        return jsonify({"Success": False, "Error": "Invalid sensor ID"})

    # print(json.dumps(json_data, indent=2))

    data_dir = current_app.config["DATA_DIR"]
    data_file = os.path.join(data_dir, "{}.txt".format(sensor_id))

    with open(data_file, "a") as f:
        # f.write(json.dumps(json_data) + "\n")
        json.dump(json_data, f)
        f.write("\n")

    return jsonify({"Success": True})

@bp.route("/log-new")
def json_transform():

    # Whether to return a json "list" or a "dict"
    return_list = False
    
    data_dir = current_app.config["DATA_DIR"]
    test_file = os.path.join(data_dir, os.listdir(data_dir)[0])

    with open(test_file, "r") as f:
        json_dumps = [json.loads(line) for line in f.readlines() if line.rstrip() != ""]

    if return_list:
        return jsonify(json_dumps)
    else:
        new_json = {snippet.pop('published_at'): snippet for snippet in json_dumps}
        return jsonify(new_json)

def gen_csv():
    pass

@bp.route('/test')
def test():
    return "Testing!"
