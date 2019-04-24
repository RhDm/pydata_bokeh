# -*- coding: utf-8 -*-

from flask import render_template
from . import plot_1_blueprint

import numpy as np
from sklearn.pipeline import make_pipeline
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Button, Slider, CheckboxGroup, Toggle
from bokeh.plotting import figure
from bokeh.themes import Theme
from scipy.stats import gamma

from bokeh.embed import components


@plot_1_blueprint.route('/')
def plot_1():

    alpha=3
    x = np.linspace(gamma.ppf(0.01, alpha), gamma.ppf(0.99, alpha), 100)
    y= gamma.pdf(x, alpha)

    p = figure(plot_width=700, plot_height=600, title="Gamma distribution")

    p.line(x=x, y=y, line_width=2)

    p.xaxis.axis_label = 'Gamma random variable'
    p.yaxis.axis_label ='Probability density'

    script_vis, div = components(p)

    return render_template('plot_1.html', script_vis=script_vis, div=div)
