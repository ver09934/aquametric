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
    # return jsonify({"uuid":uuid})
    # with open("test.txt", "a") as f:
    with open(os.path.join(os.path.dirname(__file__), "test.txt"), "a") as f:
        # f.write(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
        # f.write(" ")
        f.write(str(content).rstrip())
        f.write("\n")
    return jsonify({"Success": True})

@bp.route('/log')
def log():
    try:
        return send_file(os.path.join(os.path.dirname(__file__), "test.txt"))
    except FileNotFoundError:
        return ("Logfile does not exist.")

@bp.route('/convertlogs')
def convertlogs():
    with open(os.path.join(os.path.dirname(__file__), "test.txt"), "r") as f:
        lines_to_write = ["{" + "{".join(line.split("{")[1:]) for line in f.readlines() if "Measurement" in line]
        # NOTE: readlines does not rstrip()
    # Add jsonification step
    with open(os.path.join(os.path.dirname(__file__), "test.txt"), "w") as f:
        for line in lines_to_write:
            f.write(line)
    return "Finished!"

@bp.route('/test')
def test():
    from flask import current_app
    print(current_app.config)
    return current_app.config["DATA_DIR"]
    # return current_app.config["DATA_DIR"]
