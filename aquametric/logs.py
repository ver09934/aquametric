from flask import abort, Blueprint, current_app, jsonify, make_response, render_template, request, send_file
from io import StringIO
import os
import json
import csv

from . import util

bp = Blueprint('logs', __name__)

# --------------- OLD FUNCTIONS FOR BACKWARDS-COMPATABILITY ---------------

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

# --------------------------- END OLD FUNCTIONS ---------------------------

@bp.route('/submit-new', methods=['GET', 'POST'])
def submit_new():

    # https://flask.palletsprojects.com/en/1.1.x/api/

    data = request.get_data(as_text=True)

    # I know using eval() is a massive security hole, and I will 
    # endeavour to fix is as soon as possible, which is to say never

    print(data)

    # NEW ALGORITHM:
    # If ' in json_str:
    #   Replace all ' with ", and original " with ' in json_str
    # Run json_data = json.loads(json_str)
    # Replace all ' in json_data["data"] with "\
    # Run json_data["data"] = json.loads(json_data["data"])

    json_error_str = "Data could not be parsed into valid JSON."

    try:
        json_data = json.loads(data)
        print("Parsed JSON string using json.loads()...")
    except:
        print("Could not parse JSON string using json.loads()!")
        try:
            json_data = eval(data)
        except:
            abort(400, json_error_str)
    
    if not isinstance(json_data, dict):
        abort(400, json_error_str)

    # Original entry point:
    # json_data = request.get_json()

    try:
        if isinstance(json_data['data'], str):
            json_data['data'] = json.loads(json_data['data'])
        sensor_id = json_data['data']['id']
    except KeyError:
        abort(400, "Missing fields.")

    # print(json.dumps(json_data, indent=2))

    data_dir = current_app.config["DATA_DIR"]
    data_file = util.get_logfile_path(data_dir, sensor_id)

    with open(data_file, "a") as f:
        json.dump(json_data, f)
        f.write("\n")

    return jsonify({"Success": True})

@bp.route("/data/<sensor_id>/log.<filetype>")
def log_json(sensor_id, filetype):

    sensor_config = current_app.config["SENSOR_CONFIG"]
    data_dir = current_app.config["DATA_DIR"]
    logfile = util.get_logfile_path(data_dir, sensor_id)

    if sensor_id not in util.get_sensor_list(sensor_config):
        abort(500, "Sensor ID is not in the sensor list.")
    if not os.path.isfile(logfile):
        abort(500, "No data exists for the sensor.")
    
    with open(logfile, "r") as f:
        json_dumps = [json.loads(line) for line in f.readlines() if line.rstrip() != ""]

    if filetype == "json":

        if "latest" in request.args:
            return jsonify(json_dumps[-1])

        # Whether to return a json "list" or a "dict"
        return_list = False

        if return_list:
            return jsonify(json_dumps)
        else:
            new_json = {snippet.pop('published_at'): snippet for snippet in json_dumps}
            return jsonify(new_json)
    
    elif filetype == "csv":

        # TODO: Should put something in the util file to reformat those awful dates

        csv_IO = StringIO()
        csv_writer = csv.writer(csv_IO, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if len(json_dumps) > 0:

            header_dump = json_dumps[0]
            headers = ['published_at'] + [field for field in header_dump['data'] if field != "id"]

            csv_writer.writerow(headers)
        
            for dump in json_dumps:
                dump.update(dump.pop('data'))
                values = [dump[header] for header in headers]

                csv_writer.writerow(values)
        
        csv_IO.seek(0)
        response = make_response(csv_IO.getvalue())
        response.headers['Content-Type'] = 'text/plain'
        # response.headers['Content-Type'] = 'text/csv'
        return response

    else:
        abort(500, "Invalid log filetype.")
    
@bp.route('/test')
def test():
    return log_json("001", "json")
