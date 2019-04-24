from flask import Blueprint

plot_3_blueprint = Blueprint('plot_3', __name__)

from . import views
