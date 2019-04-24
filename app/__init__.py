from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment

bootstrap = Bootstrap()
moment = Moment()


def create_app():
    application = Flask(__name__)
    bootstrap.init_app(application)
    moment.init_app(application)

    from .main import main as main_blueprint
    application.register_blueprint(main_blueprint)

    from .plot_1 import plot_1_blueprint
    application.register_blueprint(plot_1_blueprint, url_prefix='/plot_1')

    from .plot_2 import plot_2_blueprint
    application.register_blueprint(plot_2_blueprint, url_prefix='/plot_2')

    from .plot_3 import plot_3_blueprint
    application.register_blueprint(plot_3_blueprint, url_prefix='/plot_3')


    return application
