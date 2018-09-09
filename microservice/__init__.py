from .config import DevConfig
from .models import db
from flask import Flask
from .extensions import rest_api
from .controllers.order import OrderApi, OrderDOApi
from .controllers.inout import InoutApi, InoutPIApi, InoutROApi
from .controllers.stock import StockApi
from .controllers.auth import AuthApi


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    # 注册rest_api
    # 订单
    rest_api.add_resource( OrderApi, '/api/order',  '/api/order/<string:sheetno>', endpoint='order' )
    rest_api.add_resource( OrderDOApi, '/api/order/do', '/api/order/do/<string:sheetno>', endpoint='do')
    # 出入库
    rest_api.add_resource(InoutApi,'/api/inout', '/api/inout/<string:sheetno>', endpoint='inout')
    rest_api.add_resource(InoutPIApi, '/api/inout/pi', '/api/inout/pi/<string:sheetno>', endpoint='pi')
    rest_api.add_resource(InoutROApi,'/api/inout/ro', '/api/inout/ro/<string:sheetno>', endpoint='ro')
    # 库存
    rest_api.add_resource(StockApi,'/api/stock', '/api/stock/<string:brhno>', endpoint='stock')
    # 登录验证,获取token
    rest_api.add_resource(AuthApi, '/api/auth')

    rest_api.init_app(app)
    db.init_app(app)

    @app.route('/')
    def index():
        return "hello world"


    return app
