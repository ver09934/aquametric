from flask import Blueprint, current_app, jsonify, make_response, render_template, request, send_file
from io import StringIO
import os
import json
import csv

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
        sensor_id = json_data['data']['id']
    except KeyError:
        return jsonify({"Success": False, "Error": "Missing fields"})
    # except ValueError:
    #    return jsonify({"Success": False, "Error": "Invalid sensor ID"})

    # print(json.dumps(json_data, indent=2))

    data_dir = current_app.config["DATA_DIR"]
    data_file = os.path.join(data_dir, "{}.txt".format(sensor_id))

    with open(data_file, "a") as f:
        # f.write(json.dumps(json_data) + "\n")
        json.dump(json_data, f)
        f.write("\n")

    return jsonify({"Success": True})

@bp.route("/log-json")
def log_json():

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

# TODO: Reformat those awful dates
# Should put something in the util file to do this...
@bp.route("/log-csv.csv")
def log_csv():
    
    data_dir = current_app.config["DATA_DIR"]
    test_file = os.path.join(data_dir, os.listdir(data_dir)[0])

    with open(test_file, "r") as f:
        json_dumps = [json.loads(line) for line in f.readlines() if line.rstrip() != ""]

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

@bp.route("/data/<sensor_id>/current")
def current_data():
    return "Testing!"

@bp.route('/test')
def test():
    # To demonstrate that view functions can still be called within the module...
    # Apparently I was excited about this for some reason...
    return log_json()
