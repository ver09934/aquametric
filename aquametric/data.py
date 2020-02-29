from flask import abort, Blueprint, current_app, jsonify, make_response, render_template, request, send_file
from io import StringIO, BytesIO
import os
import json
import csv
import matplotlib.pyplot as plt

from . import util

bp = Blueprint('data', __name__)

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

@bp.route('/submit-new', methods=['POST'])
def submit_new():

    json_str = request.get_data(as_text=True)

    if json_str == "":
        return jsonify({"Success": False, "Error": "No data posted"})
    
    json_data = util.load_json(json_str)
    
    if "data" in json_data:
        if isinstance(json_data["data"], str):
            json_data["data"] = util.load_json(json_data["data"])
        sensor_id = json_data['data']['id']
    else:
        return abort(400, 'JSON must contain a "data" field.')

    print(json.dumps(json_data, indent=2))

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

    if filetype == "json":
        return jsonify(util.get_json(logfile, latest=("latest" in request.args)))
    elif filetype == "csv":
        
        json_dumps = util.get_json(listform=True)
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
        # response.headers['Content-Type'] = 'text/csv' # to force download (at least in chromium)
        return response

    else:
        abort(500, "Invalid log filetype.")

@bp.route('/data/<sensor_id>/plot.png')
def graph(sensor_id):
    
    import datetime
    import pytz

    sensor_config = current_app.config["SENSOR_CONFIG"]
    data_dir = current_app.config["DATA_DIR"]
    logfile = util.get_logfile_path(data_dir, sensor_id)

    if sensor_id not in util.get_sensor_list(sensor_config):
        abort(500, "Sensor ID is not in the sensor list.")
    if not os.path.isfile(logfile):
        abort(500, "No data exists for the sensor.")

    json_data = util.get_json(util.get_logfile_path(data_dir, sensor_id))

    # TODO: Check if field is a valid data field
    # TODO: Add units
    # TODO: Add data download link
    # TODO: Add about page
    # TODO: templates in html (reduce code duplication)
    # TODO: make sidebar flash actually good

    # -------- Bad -------
    args = request.args
    field = args["field"]
    dates = []
    values = []
    for date_str, all_info in json_data.items():
        dates.append(date_str)
        values.append(all_info["data"][field])
    dates = [util.get_local_datetime(date) for date in dates]
    # ------ End Bad -----

    fig, ax = plt.subplots(figsize=(13, 3))
    
    ax.plot(dates, values, 'go-')
    ax.set_title("Graph: {} vs. Time".format(field.title()))
    ax.set_xlabel("Time")
    ax.set_ylabel("{} (Units?)".format(field.title()))
    ax.grid()

    ax.margins(x=0.01, y=0.15) # Margins are percentages
    fig.tight_layout()

    bg_color = "#ededed"
    fig.patch.set_facecolor(bg_color)
    ax.patch.set_facecolor(bg_color)

    img_io = BytesIO()
    plt.savefig(img_io, format='png', facecolor=fig.get_facecolor())
    img_io.seek(0)

    response = make_response(img_io.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response
