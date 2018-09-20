from .config import DevConfig
from .models import db
from flask import Flask
from .extensions import rest_api, apidoc
from .controllers.order import OrderApi, OrderDOApi
from .controllers.inout import InoutApi, InoutPIApi, InoutROApi
from .controllers.stock import StockApi
from .controllers.auth import AuthApi
from .controllers.index import IndexApi


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    # 注册rest_api
    # 订单
    rest_api.add_resource(OrderDOApi, '/api/order/do', '/api/order/do/', '/api/order/do/<string:sheet_no>', endpoint='do')
    # 出入库
    rest_api.add_resource(InoutPIApi, '/api/inout/pi', '/api/inout/pi/', '/api/inout/pi/<string:sheet_no>', endpoint='pi')
    rest_api.add_resource(InoutROApi, '/api/inout/ro', '/api/inout/ro/', '/api/inout/ro/<string:sheet_no>', endpoint='ro')
    # 库存
    rest_api.add_resource(StockApi,'/api/stock/', '/api/stock/<string:brh_no>', endpoint='stock')
    # 登录验证,获取token
    rest_api.add_resource(AuthApi, '/api/auth', '/api/auth/', endpoint="auth")
    # 主页
    rest_api.add_resource(IndexApi, '/')

    rest_api.init_app(app)
    apidoc.init_app(app)
    db.init_app(app)
    return app
