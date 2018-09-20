from flask_restful import Resource, marshal_with, abort
from ..models import OrderMaster
from .. import db
from .fields import OrderFields
from .parsers import OrderParse
import datetime
from .base import SheetStatus, SheetType, SheetBase
from .auth import AuthApi


class OrderApi(Resource):
    """订单api"""

    per_page = SheetBase.per_page   # 每页返回记录条数
    sheet_type = None  # 单据类型
    sheet_status = SheetStatus.approve.value  # 单据状态

    @marshal_with(OrderFields.order)
    @AuthApi.auth_required
    def get(self, sheet_no=None, user=None):

        args = OrderParse.get.parse_args()
        if not self.sheet_type:
            self.sheet_type = args['sheet_type']

        if not self.sheet_type:
            abort(400, message="无效的单据类型", code="SheetTypeRequired")

        # 登录用户，通过auth接口的token解析而得，从而进行权限控制
        if user:
            sup_no = user.get_supply()
        else:
            sup_no = None

        if sheet_no:
            order = OrderMaster.query.filter(
                OrderMaster.sheet_type == self.sheet_type,
                OrderMaster.sheet_no == sheet_no)

            if not order.first():
                abort(400, message="单据{}不存在".format(sheet_no), code="SheetNotFound")

            order = order.filter(OrderMaster.sup_no == sup_no).first()
            if not order:
                abort(403, message="权限不足", code="PermissionNotAllowed")

            # 显示供应商名称
            order.sup_name = order.supply.sup_name
            # 显示门店名称
            order.brh_name = order.branch.brh_name
            # 显示商品名称
            for detail in order.details:
                detail.item_name = detail.item.item_name
            return order
        else:
            page = args['page'] or 1
            orders = OrderMaster.query.filter(
                OrderMaster.valid_date >= datetime.datetime.now(),   # 有效期内
                OrderMaster.status == SheetStatus.approve.value,     # 审核状态
                OrderMaster.sheet_type == self.sheet_type,           # 订单类型
                OrderMaster.webapi_flag != SheetBase.flag_done_yes,  # 排除已处理
                OrderMaster.sup_no == sup_no).order_by(              #
                OrderMaster.cr_date.desc(), OrderMaster.cr_time.desc()).paginate(
                page, self.per_page)

            if orders.pages == 0:
                abort(400, message="单据第{}页不存在".format(page), code="PageOfSheetNotFound")

            for order in orders.items:
                # 显示供应商名称
                order.sup_name = order.supply.sup_name
                # 显示门店名称
                order.brh_name = order.branch.brh_name
                # 显示商品名称
                for detail in order.details:
                    detail.item_name = detail.item.item_name

            return orders.items, 200, {"pages": orders.pages, "page": page}

    @AuthApi.auth_required
    def put(self, sheet_no=None, user=None):
        if not sheet_no:
            abort(400, message="请传入有效的单据号", code="SheetNoRequired")
        if sheet_no:

            # 登录用户，通过auth接口的token解析而得，从而进行权限控制
            if user:
                sup_no = user.get_supply()
            else:
                sup_no = None

            order = OrderMaster.query.filter(OrderMaster.sheet_no == sheet_no)
            if not order.first():
                abort(400, message="单据{}不存在".format(sheet_no), code="SheetNotFound")

            order = order.filter(OrderMaster.sup_no == sup_no)
            if not order.first():
                abort(400, message="权限不足".format(sheet_no), code="PermissionNotAllowed")

            order = order.filter(OrderMaster.webapi_flag != SheetBase.flag_done_yes).first()
            if not order:
                abort(400, message="单据状态为已处理，不需要再次提交", code="SheetAlreadyDone")

            order.webapi_flag = SheetBase.flag_done_yes
            db.session.add(order)
            db.session.commit()
            return {"sheet_no": order.sheet_no, "code": "Success"}, 201


class OrderDOApi(OrderApi):
    """
        @api {get}  /api/order/do/:sheet_no 获取单据信息
        @apiVersion 1.0.0
        @apiName  DirectOrder
        @apiGroup 直配订单

        @apiPermission supply
        @apiUse  AuthRequired
        @apiUse OrderReturnParam
        @apiUse GetSheet
        @apiUse ErrorExample

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200
        {
            [{'sheet_no': '18091700DO0130', 'sheet_type': 'DO', 'sup_no': '203701', 'sup_name': '湖北致远天下贸易有限公司', 'brh_no': '9999', 'brh_name': '中百好邦干货物流仓', 'po_brh_no': '', 'sum_amt': 8324.0, 'deliver_date': '2018-09-20', 'valid_date': '2018-09-21', 'cr_date': '2018-09-17', 'cr_time': '15:41:36', 'status': '5', 'cr_oper_no': '0122', 'details': [{'line_id': 1, 'item_id': 6386, 'item_subno': '3211203450258', 'item_name': 'CASTEL卡柏莱美乐干红（木盒）750ml', 'unit_no': '瓶', 'pack_qty': 12.0, 'unit_qty': 1.0, 'qty': 12.0, 'price': 102.0, 'amt': 1224.0}, {'line_id': 2, 'item_id': 8759, 'item_subno': '8004385033310', 'item_name': '天使之手干红葡萄酒', 'unit_no': '瓶', 'pack_qty': 100.0, 'unit_qty': 1.0, 'qty': 100.0, 'price': 71.0, 'amt': 7100.0}], 'brs': [{'line_id': 1, 'item_id': 6386, 'brh_no': '0001', 'qty': 6.0}, {'line_id': 2, 'item_id': 6386, 'brh_no': '0002', 'qty': 6.0}, {'line_id': 3, 'item_id': 8759, 'brh_no': '0001', 'qty': 50.0}, {'line_id': 4, 'item_id': 8759, 'brh_no': '0002', 'qty': 50.0}]}]
        }

    """

    """
        @api {put}  /api/order/do/:sheet_no 修改处理标志
        @apiVersion 1.0.0
        @apiName  UpdateDirectOrder
        @apiGroup 直配订单

        @apiUse PutSheet
        @apiPermission supply
        @apiUse  AuthRequired
        @apiUse ErrorExample
        
         @apiSuccessExample {json} Success-Response:
         HTTP/1.1 201
        {
           "sheet_no":"1234567890"
        }
    """

    sheet_type = SheetType.do.value


