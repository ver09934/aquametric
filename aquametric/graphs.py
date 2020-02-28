from flask import Blueprint, make_response
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
