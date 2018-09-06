from flask_restful import Resource, marshal_with, abort
from ..models import OrderMaster
from .. import db
from .fields import OrderFields
from .parsers import OrderParse
import datetime
from .base import SheetStatus, SheetType, SheetBase


class OrderApi(Resource):
    """订单api"""
    # 每页返回条数
    perpage = SheetBase.per_page
    sheettype = ''
    sheetstatus = SheetStatus.approve.value

    @marshal_with(OrderFields.order)
    def get(self, sheetno=None):
        """get方法"""
        args = OrderParse.get.parse_args()
        if not self.sheettype:
            self.sheettype = args['sheettype']

        if not self.sheettype:
            abort(403, message="单据类型为空")

        if sheetno:
            order = OrderMaster.query.filter(OrderMaster.sheettype == self.sheettype).first()
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

            page = args['page'] or 1
            orders = OrderMaster.query.filter(
                OrderMaster.validdate >= datetime.datetime.now(),  # 有效期内
                OrderMaster.status == SheetStatus.approve.value,   # 审核状态
                OrderMaster.sheettype == self.sheettype,           # 订单类型
                OrderMaster.webapiflag != '1').order_by(           # 未处理的订单
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
            abort(400, message="请传入有效的单据号")
        if sheetno:
            order = OrderMaster.query.get(sheetno)
            if not order:
                abort(404, message="订单{}不存在".format(sheetno))
            order.webapiflag = SheetBase.flag_done_yes
            db.session.add(order)
            db.session.commit()
            return order.sheetno


class OrderDOApi(OrderApi):
    """直配订单"""
    sheettype = SheetType.do.value


