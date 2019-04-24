# -*- coding: utf-8 -*-

from flask import render_template# , url_for, flash, request, jsonify
from . import plot_3_blueprint


import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures

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

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from threading import Thread

import warnings
warnings.filterwarnings('ignore')


def data_no_noise(x, a, b, c):
    return a * np.exp(-b * x) + c
    #return 5+2.5*np.sin(0.1*x)+0.5

def generate_data_no_noise(datapoints):
    x = np.linspace(0, 50, datapoints)
    y = data_no_noise(x, 2.5, 1.3, 0.5)
    return x, y  

def generate_data_w_noise(datapoints):
    x, y = generate_data_no_noise(datapoints)
    y_noise = 0.2 * np.random.normal(size=x.size)
    y_with_noise = y + y_noise
    return x, y_with_noise

def cerate_poly_model(degree, x, y):
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(x.reshape(len(x),1), y.reshape(len(x),1))
    y_pred_poly = model.predict(x.reshape(len(x),1))
    return y_pred_poly
    
def plot_poly_model(doc):
    
    #initial data and polynomial
    x, y= generate_data_w_noise(100)
    y_data = cerate_poly_model(3, x, y)    
    p = figure(plot_width=400, plot_height=400, x_axis_label='x', y_axis_label='y',
               tools="pan,wheel_zoom,reset,save", x_range=(-1,51)) #y_range=(0,3), x_range=(-1,51)
    source = ColumnDataSource(data={
        'y_data': y_data.ravel(),
        'x_1': x,
        'y_2': y})
    
    p.circle(x='x_1', y='y_2', legend="", fill_color="#1f78b4", line_color="#1f78b4", size=6,
             fill_alpha=0.2, source=source)
    p.line(x='x_1', y='y_data', legend="", line_color="#ef8a62", line_width=4, source= source)
    
    def callback_fix_y_axis():
        p.y_range.start = 0
        p.y_range.end = 3
            
    def callback_deg(attr, old, new):
        y_data= cerate_poly_model(new, source.data['x_1'], source.data['y_2'])    
        new_source= ColumnDataSource(data={
            'y_data': y_data.ravel(),
            'x_1': source.data['x_1'],
            'y_2': source.data['y_2']})   
        source.data.update(new_source.data)

    def callback_data():
        x, y= generate_data_w_noise(slider_num_datapoints.value)
        y_data = cerate_poly_model(slider_deg.value, source.data['x_1'], source.data['y_2'])  
        source.data= ColumnDataSource(data={
            'y_data': y_data.ravel(),
            'x_1': x,
            'y_2': y}).data
        
    def callback_data_n(attr, old, new):
        x, y= generate_data_w_noise(new)
        y_data = cerate_poly_model(slider_deg.value, source.data['x_1'], source.data['y_2'])  
        source.data= ColumnDataSource(data={
            'y_data': y_data.ravel(),
            'x_1': x,
            'y_2': y}).data
            
    slider_deg = Slider(start=1, end=50, value=3, step=1, title="Polynomial degree")
    slider_deg.on_change('value', callback_deg)
    
    slider_num_datapoints = Slider(start=50, end=1000, value=100, step=10, title="Number of data points")
    slider_num_datapoints.on_change('value', callback_data_n)
    
    button_gen = Button(label="Generate new data", button_type="default")
    button_gen.on_click(callback_data)
    
    button_range = Button(label="Fix axis range", button_type="default")
    button_range.on_click(callback_fix_y_axis)
    
    doc.add_root(column(row(slider_deg, slider_num_datapoints, button_gen), button_range, p))
    doc.theme = Theme(json=yaml.load("""
        attrs:
            Figure:
                height: 600
                width: 800
    """))


bkapp = Application(FunctionHandler(plot_poly_model))

sockets, port = bind_sockets("localhost", 0)

@plot_3_blueprint.route('/', methods=['GET'])
def bkapp_page():
    script_vis = server_document('http://localhost:%d/bkapp' % port)
    return render_template("plot_3.html", script_vis=script_vis)

def bk_worker():
    asyncio.set_event_loop(asyncio.new_event_loop())

    bokeh_tornado = BokehTornado({'/bkapp': bkapp}, extra_websocket_origins=["localhost:8000"])
    bokeh_http = HTTPServer(bokeh_tornado)
    bokeh_http.add_sockets(sockets)

    server = BaseServer(IOLoop.current(), bokeh_tornado, bokeh_http)
    server.start()
    server.io_loop.start()

Thread(target=bk_worker).start()

