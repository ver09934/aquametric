import matplotlib.pyplot as plt
import numpy as np
from flask import Blueprint, make_response, render_template
from io import BytesIO

# url_prefix="/graph"
bp = Blueprint(__name__, __name__)

@bp.route('/graph.png')
def index():

    img_io = BytesIO()
    
    x = np.linspace(0, 10)
    y = np.sin(x)
    plt.plot(x, y, 'go-')
    plt.title("Real Aquametric Data")
    plt.savefig(img_io, format='png')

    img_io.seek(0)

    response = make_response(img_io.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response
