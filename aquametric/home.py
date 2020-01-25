from flask import Blueprint, make_response, render_template, jsonify, request, send_file
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import os

bp = Blueprint(__name__, __name__)

@bp.route('/')
def index():
    return render_template('index.html', table=get_table())

def get_table():
    # df = pd.DataFrame([i**2 for i in range(11)])
    df = pd.DataFrame(np.random.randint(low=1, high=100, size=10))
    return df.to_html()

@bp.route('/graph.png')
def test():

    img_io = BytesIO()

    plt.clf()
    
    x = np.linspace(0, 30, num=30)
    # y = np.sin(x)
    y = np.random.randint(low=1, high=100, size=len(x))
    plt.plot(x, y, 'go-')
    plt.title("Real Aquametric Data")
    plt.savefig(img_io, format='png')

    img_io.seek(0)

    response = make_response(img_io.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@bp.route('/submit', methods=['GET', 'POST'])
def submit():
    content = request.get_json(silent=False)
    # return jsonify({"uuid":uuid})
    # with open("test.txt", "a") as f:
    with open(os.path.join(os.path.dirname(__file__), "test.txt"), "a") as f:
        f.write(str(content))
        f.write("\n")
    return jsonify({"Success": True})

@bp.route('/log')
def log():
    try:
        return send_file("../test.txt")
    except FileNotFoundError:
        return ("Logfile does not exist.")
