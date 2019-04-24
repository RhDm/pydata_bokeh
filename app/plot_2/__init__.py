from flask import Blueprint

plot_2_blueprint = Blueprint('plot_2', __name__)

from . import views
