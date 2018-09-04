from microservice.config import DevConfig
from microservice.models import db
from flask import Flask
from microservice.extensions import rest_api
from microservice.controllers.order import OrderApi


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)
    # 注册rest_api
    rest_api.add_resource(
        OrderApi,
        '/api/order',
        '/api/order/<string:sheetno>',
        endpoint='api'
    )
    rest_api.init_app(app)
    db.init_app(app)

    @app.route('/')
    def index():
        return "hello world"


    return app
