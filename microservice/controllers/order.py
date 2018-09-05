from flask_restful import Resource, marshal_with, abort
from ..models import OrderMaster, SheetStatus, OrderType
from .. import db
from .fields import OrderFields
from .parsers import OrderParse
import datetime


class OrderApi(Resource):
    """订单api"""
    # 每页返回条数
    perpage = 5

    @marshal_with(OrderFields.order)
    def get(self, sheetno=None):
        if sheetno:
            order = OrderMaster.query.get(sheetno)
            if not order:
                abort(404, message="订单{}不存在".format(sheetno))
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
            orders = OrderMaster.query.filter(
                OrderMaster.validdate >= datetime.datetime.now(),  # 有效期内
                OrderMaster.status == SheetStatus.approve.value,   # 审核状态
                OrderMaster.sheettype == OrderType.do.value,       # 直配订单
                OrderMaster.webapiflag != '1').order_by(           # 未处理
                OrderMaster.crdate.desc(), OrderMaster.crtime.desc()).paginate(
                page, self.perpage)

            if orders.pages == 0:
                abort(404, message="订单第{}页不存在".format(page))

            for order in orders.items:
                # 显示供应商名称
                order.supname = order.supply.supname
                # 显示门店名称
                order.brhname = order.branch.brhname
                # 显示商品名称
                for detail in order.details:
                    detail.itemname = detail.item.itemname

            return orders.items, 200, {"pages": orders.pages, "page": page}

    def put(self, sheetno=None):
        if not sheetno:
            abort(400)
        if sheetno:
            order = OrderMaster.query.get(sheetno)
            if not order:
                abort(404, message="订单{}不存在".format(sheetno))
            order.webapiflag = '1'
            db.session.add(order)
            db.session.commit()
            return order.sheetno, 200





