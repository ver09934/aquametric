from flask import Blueprint, render_template, jsonify, request, send_file
import os
import datetime

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

    # TODO: Parse json to determine log file name
    # TODO: Check if is valid JSON
    # TODO: Check if json contains an ID string

    with open(os.path.join(os.path.dirname(__file__), "test.txt"), "a") as f:
        f.write(str(content).rstrip())
        f.write("\n")
    
    return jsonify({"Success": True})

# TODO: Unit page will have links to raw log files
# TODO: Have JSON and CSV download options (CSV auto-generated on the fly...)
@bp.route('/log')
def log():
    try:
        return send_file(os.path.join(os.path.dirname(__file__), "test.txt"))
    except FileNotFoundError:
        return ("Logfile does not exist.")

@bp.route('/test')
def test():
    from flask import current_app
    return current_app.config["DATA_DIR"]
