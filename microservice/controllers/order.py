from flask_restful import Resource, marshal_with, abort
from microservice.models import Order
from microservice.controllers.fields import OrderFields
from microservice.controllers.parsers import OrderParse
from microservice import db


class OrderApi(Resource):
    """订单api"""
    # 每页返回条数
    perpage = 5

    @marshal_with(OrderFields.order)
    def get(self, sheetno=None):
        if sheetno:
            order = Order.query.get(sheetno)
            if not order:
                abort(404, message="订单{}不存在".format(sheetno))
                return order
            # 显示供应商名称
            order.supname = order.supply.supname
            # 显示门店名称
            order.brhname = order.branch.brhname
            # 显示商品名称
            for detail in order.details:
                detail.itemname = detail.item.itemname
            return order
        else:
            args = OrderParse.get.parse_args()
            page = args['page'] or 1
            orders = Order.query.order_by(Order.crdate.desc(), Order.crtime.desc()).paginate(page, self.perpage)
            for order in orders.items:
                # 显示供应商名称
                order.supname = order.supply.supname
                # 显示门店名称
                order.brhname = order.branch.brhname
                # 显示商品名称
                for detail in order.details:
                    detail.itemname = detail.item.itemname
            return orders.items

    def put(self, sheetno):
        if sheetno:
            order = Order.query.get(sheetno)
            if not order:
                abort(404, message="订单{}不存在".format(sheetno))
                return
            order.webapiflag = '1'
            db.session.add(order)
            db.session.commit()
            return order.sheetno, 200





