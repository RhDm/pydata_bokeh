import json

from flask import Flask
from gevent.pywsgi import WSGIServer

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import json_item
from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.sampledata.autompg import autompg
from scipy.stats import gamma
import numpy as np

from numpy import cos, linspace
from flask_cors import CORS

app = Flask(__name__)
# CORS enabled so react frontend can pull data from python backend
CORS(app)

@app.route('/')
def hello_world():
    return ''


@app.route('/plot')
def plot():
    # copy/pasted from Bokeh 'JavaScript Callbacks' - used as an example
    # https://bokeh.pydata.org/en/latest/docs/user_guide/interaction/callbacks.html

    alpha=3
    x = np.linspace(gamma.ppf(0.01, alpha), gamma.ppf(0.99, alpha), 100)
    y= gamma.pdf(x, alpha)

    p = figure(plot_width=700, plot_height=600, title="Gamma distribution")

    p.line(x=x, y=y, line_width=2)

    p.xaxis.axis_label = 'Gamma random variable'
    p.yaxis.axis_label ='Probability density'


    return json.dumps(json_item(p, "myplot"))


# Using WSGI server to allow self contained server
print("Listening on HTTP port 5000")
http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()