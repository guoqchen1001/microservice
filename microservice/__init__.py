from .config import DevConfig
from .models import db
from flask import Flask
from .extensions import rest_api
from .controllers.order import OrderApi
from .controllers.inout import InoutApi


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)
    # 注册rest_api
    rest_api.add_resource(
        OrderApi,
        '/api/order',
        '/api/order/<string:sheetno>',
        endpoint='order'
    )

    rest_api.add_resource(
        InoutApi,
        '/api/inout',
        '/api/inout/<string:sheetno>',
        endpoint='inout'

    )
    rest_api.init_app(app)
    db.init_app(app)

    @app.route('/')
    def index():
        return "hello world"


    return app
