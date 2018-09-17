from flask_restful import Resource, marshal_with, abort
from ..models import OrderMaster
from .. import db
from .fields import OrderFields
from .parsers import OrderParse
import datetime
from .base import SheetStatus, SheetType, SheetBase, UserPower
from .auth import AuthApi



class OrderApi(Resource):
    """订单api"""

    per_page = SheetBase.per_page   # 每页返回记录条数
    sheet_type = ''  # 单据类型
    sheet_status = SheetStatus.approve.value  # 单据状态

    @marshal_with(OrderFields.order)
    @AuthApi.auth_required
    def get(self, sheet_no=None, user_no=None):
        """
        @api {get}  /api/order/:sheet_no 获取订单信息
        @apiVersion 1.0.0
        @apiName  order
        @apiGroup 订单

        @apiPermission supply
        @apiUse  AuthRequired
        @apiUse OrderReturnParam
        @apiUse GetSheet
        @apiUse GetSheetByType

        @apiSuccessExample {json} Success-Response:
        {
            [{'sheet_no': '18091700DO0130', 'sheet_type': 'DO', 'sup_no': '203701', 'sup_name': '湖北致远天下贸易有限公司', 'brh_no': '9999', 'brh_name': '中百好邦干货物流仓', 'po_brh_no': '', 'sum_amt': 8324.0, 'deliver_date': '2018-09-20', 'valid_date': '2018-09-21', 'cr_date': '2018-09-17', 'cr_time': '15:41:36', 'status': '5', 'cr_oper_no': '0122', 'details': [{'line_id': 1, 'item_id': 6386, 'item_subno': '3211203450258', 'item_name': 'CASTEL卡柏莱美乐干红（木盒）750ml', 'unit_no': '瓶', 'pack_qty': 12.0, 'unit_qty': 1.0, 'qty': 12.0, 'price': 102.0, 'amt': 1224.0}, {'line_id': 2, 'item_id': 8759, 'item_subno': '8004385033310', 'item_name': '天使之手干红葡萄酒', 'unit_no': '瓶', 'pack_qty': 100.0, 'unit_qty': 1.0, 'qty': 100.0, 'price': 71.0, 'amt': 7100.0}], 'brs': [{'line_id': 1, 'item_id': 6386, 'brh_no': '0001', 'qty': 6.0}, {'line_id': 2, 'item_id': 6386, 'brh_no': '0002', 'qty': 6.0}, {'line_id': 3, 'item_id': 8759, 'brh_no': '0001', 'qty': 50.0}, {'line_id': 4, 'item_id': 8759, 'brh_no': '0002', 'qty': 50.0}]}]
        }

        """
        args = OrderParse.get.parse_args()
        if not self.sheet_type:
            self.sheet_type = args['sheet_type']

        if not self.sheet_type:
            abort(400, message="无效的单据类型")

        # 登录用户，通过auth接口的token解析而得，从而进行权限控制
        if user_no:
            user_power = UserPower(user_no)
            sup_no = user_power.get_supno()
        else:
            sup_no = ""

        if sheet_no:
            order = OrderMaster.query.filter(
                OrderMaster.sheet_type == self.sheet_type,
                OrderMaster.sheet_no == sheet_no,
                OrderMaster.sup_no == sup_no).first()
            if not order:
                abort(400, message="订单{}不存在".format(sheet_no))
            # 显示供应商名称
            order.sup_name = order.supply.supname
            # 显示门店名称
            order.brh_name = order.branch.brhname
            # 显示商品名称
            for detail in order.details:
                detail.item_name = detail.item.itemname
            return order
        else:
            page = args['page'] or 1
            orders = OrderMaster.query.filter(
                OrderMaster.valid_date >= datetime.datetime.now(),  # 有效期内
                OrderMaster.status == SheetStatus.approve.value,   # 审核状态
                OrderMaster.sheet_type == self.sheet_type,           # 订单类型
                OrderMaster.webapi_flag != '1',
                OrderMaster.sup_no == sup_no).order_by(           # 未处理的订单
                OrderMaster.cr_date.desc(), OrderMaster.cr_time.desc()).paginate(
                page, self.per_page)

            if orders.pages == 0:
                abort(400, message="订单第{}页不存在".format(page))

            for order in orders.items:
                # 显示供应商名称
                order.sup_name = order.supply.supname
                # 显示门店名称
                order.brh_name = order.branch.brhname
                # 显示商品名称
                for detail in order.details:
                    detail.item_name = detail.item.itemname

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
    """
       @api {get}  /api/order/do/:sheet_no 直配订单
       @apiVersion 1.0.0
       @apiName  order_do
       @apiGroup 订单
       @apiParam  (入参) {int}  page=1  页数
       @apiParam  (入参) {string} sheet_no 单号,不传入则返回单据列表
       @apiPermission supply
       @apiSuccessExample {json} Success-Response:
       {
           [{'sheet_no': '18091700DO0130', 'sheet_type': 'DO', 'sup_no': '203701', 'sup_name': '湖北致远天下贸易有限公司', 'brh_no': '9999', 'brh_name': '中百好邦干货物流仓', 'po_brh_no': '', 'sum_amt': 8324.0, 'deliver_date': '2018-09-20', 'valid_date': '2018-09-21', 'cr_date': '2018-09-17', 'cr_time': '15:41:36', 'status': '5', 'cr_oper_no': '0122', 'details': [{'line_id': 1, 'item_id': 6386, 'item_subno': '3211203450258', 'item_name': 'CASTEL卡柏莱美乐干红（木盒）750ml', 'unit_no': '瓶', 'pack_qty': 12.0, 'unit_qty': 1.0, 'qty': 12.0, 'price': 102.0, 'amt': 1224.0}, {'line_id': 2, 'item_id': 8759, 'item_subno': '8004385033310', 'item_name': '天使之手干红葡萄酒', 'unit_no': '瓶', 'pack_qty': 100.0, 'unit_qty': 1.0, 'qty': 100.0, 'price': 71.0, 'amt': 7100.0}], 'brs': [{'line_id': 1, 'item_id': 6386, 'brh_no': '0001', 'qty': 6.0}, {'line_id': 2, 'item_id': 6386, 'brh_no': '0002', 'qty': 6.0}, {'line_id': 3, 'item_id': 8759, 'brh_no': '0001', 'qty': 50.0}, {'line_id': 4, 'item_id': 8759, 'brh_no': '0002', 'qty': 50.0}]}]
       }
       @apiErrorExample {json} Error-Response:
       HTTP/1.1 400 Not Found
       {
           "message": "订单1234567890不存在"
       }
       HTTP/1.1 400 Not Found
       {
           "message": "订单第2页不存在"
       }
    """
    sheet_type = SheetType.do.value


