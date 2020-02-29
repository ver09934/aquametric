from flask import Blueprint, make_response, request
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

bp = Blueprint('graphs', __name__, url_prefix="/graph")

@bp.route('/test.png')
def test():

    fig, ax = plt.subplots(figsize=(13, 3))
    
    ax.plot(np.random.randint(low=1, high=100, size=30), 'go-')
    ax.set_title("Test Graph: Random Values")
    ax.set_xlabel("X Label")
    ax.set_ylabel("Y Label")

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

@bp.route('/<sensor_id>/plot.png')
def graph(sensor_id):

    import requests
    import json
    from flask import url_for
    import datetime
    import pytz
    
    json_data = json.loads(requests.get("http://localhost:5000" + url_for("logs.log_json", sensor_id=sensor_id, filetype="json")).text)

    # TODO: Check if unit with sensor ID exists
    # (may want to put this into a method in the util...)

    print(json_data)

    args = request.args
    field = args["field"]

    print(field)

    # TODO: Check if field is a valid data field

    dates = []
    values = []
    for date_str, all_info in json_data.items():
        dates.append(date_str)
        values.append(all_info["data"][field])
    
    dates = [datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f%z') for date in dates]
    dates = [date.astimezone(pytz.timezone('US/Eastern')) for date in dates]
    print(dates)
    print(values)

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
