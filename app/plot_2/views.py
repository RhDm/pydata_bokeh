# -*- coding: utf-8 -*-

# as in https://github.com/bokeh/bokeh/blob/master/examples/howto/server_embed/flask_gunicorn_embed.py

from flask import render_template# , url_for, flash, request, jsonify
from . import plot_2_blueprint

import numpy as np
from scipy.stats import gamma

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Button, Slider, CheckboxGroup, Toggle
from bokeh.plotting import figure
from bokeh.themes import Theme
import yaml

import asyncio

from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import server_document
from bokeh.server.server import BaseServer
from bokeh.server.tornado import BokehTornado
from bokeh.server.util import bind_sockets

# from bokeh.server.server import Server
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from threading import Thread


def gamma_shape(doc):
    alpha=3
    x = np.linspace(0, gamma.ppf(0.999, alpha), 100)
    y= gamma.pdf(x, alpha)
    
    source = ColumnDataSource(data={
        'x_1': x,
        'y_1': y})

    # tooltips_formatting =[('random variable', '@x_1'), ('PD', '@y_1')]
    # or
    tooltips_formatting ="""
                        <div>
                            <div>
                                <span style="font-size: 14px; color: #3c6978">random variable: </span>
                                <span style="font-size: 14px; float: right;  margin: 0px 0px 0px 15px">@x_1</span>
                            </div>
                            <div>
                                <span style="font-size: 14px; color: #3c6978">max:</span>
                                <span style="font-size: 14px; float: right; margin: 0px 0px 0px 15px">@y_1</span>
                            </div>
                        </div>
                        """

    p = figure(plot_width=700, plot_height=600, title="Gamma distribution", tooltips= tooltips_formatting)

    p.line(x='x_1', y='y_1', line_width=2, source= source)
    
    p.x_range.start = 0
    p.xaxis.axis_label = 'Gamm random variable'
    p.yaxis.axis_label ='Probability density'

    def callback_shape(attr, old, new):
        x_updated = np.linspace(0, gamma.ppf(0.999, new), 100)
        y_updated= gamma.pdf(source.data['x_1'], new)
        new_source= ColumnDataSource(data={
            'x_1': x_updated,
            'y_1': y_updated})   
        source.data.update(new_source.data)

    slider_shape = Slider(start=1, end=30, value=3, step=.1, title="Gamma shape")
    slider_shape.on_change('value', callback_shape)

    doc.add_root(column(slider_shape, p))
    doc.theme = Theme(json=yaml.load("""
            attrs:
                Figure:
                    height: 600
                    width: 800
        """))

bkapp = Application(FunctionHandler(gamma_shape))

sockets, port = bind_sockets("localhost", 0)

@plot_2_blueprint.route('/', methods=['GET'])
def bkapp_page():
    script_vis = server_document('http://localhost:%d/bkapp' % port)
    return render_template("plot_2.html", script_vis=script_vis)

def bk_worker():
    asyncio.set_event_loop(asyncio.new_event_loop())

    bokeh_tornado = BokehTornado({'/bkapp': bkapp}, extra_websocket_origins=["localhost:8000"])
    bokeh_http = HTTPServer(bokeh_tornado)
    bokeh_http.add_sockets(sockets)

    server = BaseServer(IOLoop.current(), bokeh_tornado, bokeh_http)
    server.start()
    server.io_loop.start()

Thread(target=bk_worker).start()












