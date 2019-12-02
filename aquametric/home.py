from flask import Blueprint, render_template
import pandas as pd

bp = Blueprint(__name__, __name__)

@bp.route('/')
def index():

    return render_template('index.html', table=get_table())

def get_table():

    df = pd.DataFrame([i**2 for i in range(11)])
    return df.to_html()
