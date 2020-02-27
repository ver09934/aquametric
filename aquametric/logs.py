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

    json_data = request.get_json(silent=False)

    # NOTE: May want to remove conversion of sensor ID to int, allowing for
    # sensor ID strings which are not strings which can be converted to integers.
    # Would be able to remove ValueError handling if we did this.
    # update: This has now been done!

    try:
        json_data['data'] = json.loads(json_data['data'])
        # sensor_id = int(json_data['data']['id'])
        # If integer, "{:03d}.txt".format(int(sensor_id))
        sensor_id = json_data['data']['id']
    except KeyError:
        return jsonify({"Success": False, "Error": "Missing fields"})
    # except ValueError:
    #    return jsonify({"Success": False, "Error": "Sensor ID not an integer"})

    # print(json.dumps(json_data, indent=2))

    data_dir = current_app.config["DATA_DIR"]
    data_file = util.get_logfile_path(data_dir, sensor_id)

    with open(data_file, "a") as f:
        # f.write(json.dumps(json_data) + "\n")
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
        return response

    else:
        abort(500, "Invalid log filetype.")
    
@bp.route('/test')
def test():
    return log_json("001", "json")
