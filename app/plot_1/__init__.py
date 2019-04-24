from flask import Blueprint

plot_1_blueprint = Blueprint('plot_1', __name__)

from . import views
