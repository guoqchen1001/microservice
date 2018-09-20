from flask_restful import Resource, marshal_with, abort
from ..models import Supply, Branch, Item,  BrDynamic, DynamicInoutMaster, DynamicInoutDetail
from .fields import InoutFields
from .. import db
from .parsers import InoutParser
from operator import attrgetter
from .base import SheetStatus, SheetSlice, SheetType, SheetBase, ErrorCode
from .auth import AuthApi


class InoutApi(Resource):
    """出入库"""
    per_page = SheetBase.per_page
    sheet_type = None
    status = SheetStatus.approve.value
    br_dynamic_list = None

    @marshal_with(InoutFields.inoutmaster)
    @AuthApi.auth_required
    def get(self, sheet_no=None, user=None):
        """get方法"""
        args = InoutParser.get.parse_args()

        if not self.sheet_type:
            self.sheet_type = args['sheet_type'] or None

        if not self.sheet_type:
            abort(403, message="无效的单据类型", code=ErrorCode.sheet_type_required.value)

        # 登录用户，通过auth接口的token解析而得，从而进行权限控制
        if user:
            sup_no = user.get_supply()
        else:
            sup_no = None

        if sheet_no:
            # 根据单号获取分组表序号
            # 验证单号合法性
            if not SheetBase.sheet_no_validator(sheet_no):
                abort(400, message="单号不合法",code=ErrorCode.sheet_no_not_valid.value)

            grp_no = sheet_no[SheetSlice.sheet_grp_slice]
            Master = DynamicInoutMaster(grp_no=grp_no).model()
            Dbranch = db.aliased(Branch)
            result = db.session.query(Master, Supply, Branch, Dbranch).outerjoin(
                Supply, Master.sup_no == Supply.sup_no).outerjoin(
                Branch, Master.brh_no == Branch.brh_no).outerjoin(
                Dbranch, Master.d_brh_no == Dbranch.brh_no
            ).filter(Master.sheet_no == sheet_no,
                     Master.sheet_type == self.sheet_type,
                     Master.webapi_flag != SheetBase.flag_done_yes)

            if not result.first():
                abort(400, message="单号{}不存在".format(sheet_no), code=ErrorCode.sheet_not_found.value)

            result = result.filter(Master.sup_no.in_(sup_no)).first()
            if not result:
                abort(401, message="权限不足", code=ErrorCode.permission_not_allowed.value)
            master, supply, branch, d_branch = result

            if supply:
                master.sup_name = supply.sup_name
            if branch:
                master.brh_name = branch.brh_name
            if d_branch:
                master.d_brh_name = d_branch.brh_name

            details = master.details
            items = Item.query.filter(Item.item_id.in_([detail.item_id for detail in details]))
            for item in items:
                for detail in details:
                    if item.item_id == detail.item_id:
                        detail.item_name = item.item_name

            return master
        else:
            args = InoutParser.get.parse_args()
            page = args['page'] or 1
            brh_no = args['brh_no'] or None

            if brh_no:
                # 根据门店来确定分组
                Master = DynamicInoutMaster(brh_no=brh_no).model()
                Dbranch = db.aliased(Branch)

                # 查询出入库单据
                result = db.session.query(Master, Supply, Branch, Dbranch).outerjoin(
                Supply, Master.sup_no == Supply.sup_no).outerjoin(
                Branch, Master.brh_no == Branch.brh_no).outerjoin(
                Dbranch, Master.d_brh_no == Dbranch.brh_no).filter(
                    Master.sheet_type == self.sheet_type,
                    Master.status == self.status,
                    Master.sup_no.in_(sup_no),
                    Master.webapi_flag != SheetBase.flag_done_yes).order_by(
                    Master.cr_date.desc(), Master.cr_time.desc()
                )

                # 不存在则返回
                if not result.first():
                    abort(400, message="单据第{}页不存在".format(page), code=ErrorCode.page_of_sheet_not_found.value)

                # 最终返回数据s
                master_all = []

                result = result.all()
                # 更新供应商名称，机构名称，目的机构名称，商品名称
                for master, supply, branch, d_branch in result[self.per_page*(page - 1):self.per_page*page]:
                    # 取供应商名称
                    if supply:
                        master.sup_name = supply.sup_name

                    # 取机构名称
                    if branch:
                        master.brh_name = branch.brh_name

                    # 取目的机构名称
                    if d_branch:
                        master.d_brh_name = d_branch.brh_name

                    # 查询商品名称
                    for detail in master.details:
                        item = Item.query.get(detail.item_id)
                        if item:
                            detail.item_name = item.item_name

                    master_all.append(master)

                return master_all

            else:
                # 没有传入门店

                # 如果制定了分组表
                if self.br_dynamic_list is None:
                    br_dynamic_list = db.session.query(BrDynamic.dynamic_grp).distinct().all()
                else:
                    br_dynamic_list = self.br_dynamic_list

                master_all = []
                for br_dynamic in br_dynamic_list:
                    Master = DynamicInoutMaster(grp_no=br_dynamic.dynamic_grp).model()
                    Dbranch = db.aliased(Branch)
                    result = db.session.query(Master, Supply, Branch, Dbranch).outerjoin(
                            Supply, Master.sup_no == Supply.sup_no).outerjoin(
                            Branch, Master.brh_no == Branch.brh_no).outerjoin(
                            Dbranch, Master.d_brh_no == Dbranch.brh_no).filter(
                            Master.sheet_type == self.sheet_type,
                            Master.sup_no.in_(sup_no),
                            Master.status == self.status,
                            Master.webapi_flag != SheetBase.flag_done_yes).order_by(
                            Master.cr_date.desc(), Master.cr_time.desc()).limit(page*self.per_page).all()
                    master_one_grp = []
                    for master, supply, branch, d_branch in result:
                        if supply:
                            master.sup_name = supply.sup_name
                        if branch:
                            master.brh_name = branch.brh_name
                        if d_branch:
                            master.brh_name = d_branch.brh_name
                        # 每个分组取前n页数据

                        details = master.details
                        for detail in details:
                            item = Item.query.get(detail.item_id)
                            detail.item_name = item.item_name
                        master_one_grp.append(master)

                    master_all.extend(master_one_grp)

                master_all = sorted(master_all, key=attrgetter('cr_date', 'cr_time'), reverse=True)

                if not master_all[self.per_page*(page - 1):self.per_page*page]:
                    abort(400, message="单据第{}页不存在".format(page), code=ErrorCode.page_of_sheet_not_found.value)

                return master_all[self.per_page*(page - 1):self.per_page*page]

    @AuthApi.auth_required
    def put(self, sheet_no=None, user=None):
        """put方法"""

        sup_no = user.get_supply()

        if not sheet_no:
            abort(400, message="请传入有效的单据号")

        if sheet_no:
            if not SheetBase.sheet_no_validator(sheet_no):
                abort(400, message="单号无效", code=ErrorCode.sheet_no_not_valid)

            grp_no = sheet_no[SheetSlice.sheet_grp_slice]
            Master = DynamicInoutMaster(grp_no=grp_no).model()
            master = Master.query.get(sheet_no)

            if not master or master.sheet_type != self.sheet_type:
                abort(400, message="单据{}不存在".format(sheet_no),code=ErrorCode.sheet_not_found)

            if master.webapi_flag == SheetBase.flag_done_yes:
                abort(400, message="单据{}已处理，不需要重复提交".format(sheet_no), code=ErrorCode.sheet_already_done.value)

            if master.sup_no not in sup_no:
                abort(400, messgae="权限不足", code=ErrorCode.permission_not_allowed.value)

            master.webapi_flag = SheetBase.flag_done_yes
            db.session.add(master)
            db.session.commit()

            return dict(sheet_no=master.sheet_no,code="Success")


class InoutPIApi(InoutApi):
    """
        @api {get}  /api/inout/pi/<string:sheet_no>  获取单据信息
        @apiVersion 1.0.0
        @apiName  GetPurchaseIn
        @apiGroup 采购收货单

        @apiPermission supply
        @apiUse  AuthRequired
        @apiUse GetSheet
        @apiUse ErrorExample
        @apiUse InoutReturnParam

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200
        {
            [{'sheet_no': '18091700DO0130', 'sheet_type': 'DO', 'sup_no': '203701', 'sup_name': '湖北致远天下贸易有限公司', 'brh_no': '9999', 'brh_name': '中百好邦干货物流仓', 'po_brh_no': '', 'sum_amt': 8324.0, 'deliver_date': '2018-09-20', 'valid_date': '2018-09-21', 'cr_date': '2018-09-17', 'cr_time': '15:41:36', 'status': '5', 'cr_oper_no': '0122', 'details': [{'line_id': 1, 'item_id': 6386, 'item_subno': '3211203450258', 'item_name': 'CASTEL卡柏莱美乐干红（木盒）750ml', 'unit_no': '瓶', 'pack_qty': 12.0, 'unit_qty': 1.0, 'qty': 12.0, 'price': 102.0, 'amt': 1224.0}, {'line_id': 2, 'item_id': 8759, 'item_subno': '8004385033310', 'item_name': '天使之手干红葡萄酒', 'unit_no': '瓶', 'pack_qty': 100.0, 'unit_qty': 1.0, 'qty': 100.0, 'price': 71.0, 'amt': 7100.0}], 'brs': [{'line_id': 1, 'item_id': 6386, 'brh_no': '0001', 'qty': 6.0}, {'line_id': 2, 'item_id': 6386, 'brh_no': '0002', 'qty': 6.0}, {'line_id': 3, 'item_id': 8759, 'brh_no': '0001', 'qty': 50.0}, {'line_id': 4, 'item_id': 8759, 'brh_no': '0002', 'qty': 50.0}]}]
        }

    """

    """
        @api {put}  /api/inout/pi/<string:sheet_no>  修改处理标志
        @apiVersion 1.0.0
        @apiName  UpdatePurchaseIn
        @apiGroup 采购收货单

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
    sheet_type = SheetType.pi.value


class InoutROApi(InoutApi):
    """
        @api {get}  /api/inout/ro/<string:sheet_no>   获取单据信息
        @apiVersion 1.0.0
        @apiName  ReturnOut
        @apiGroup 采购退货单

        @apiPermission supply
        @apiUse  AuthRequired
        @apiUse GetSheet
        @apiUse ErrorExample
        @apiUse InoutReturnParam

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200
        {
            [{'sheet_no': '18091700DO0130', 'sheet_type': 'DO', 'sup_no': '203701', 'sup_name': '湖北致远天下贸易有限公司', 'brh_no': '9999', 'brh_name': '中百好邦干货物流仓', 'po_brh_no': '', 'sum_amt': 8324.0, 'deliver_date': '2018-09-20', 'valid_date': '2018-09-21', 'cr_date': '2018-09-17', 'cr_time': '15:41:36', 'status': '5', 'cr_oper_no': '0122', 'details': [{'line_id': 1, 'item_id': 6386, 'item_subno': '3211203450258', 'item_name': 'CASTEL卡柏莱美乐干红（木盒）750ml', 'unit_no': '瓶', 'pack_qty': 12.0, 'unit_qty': 1.0, 'qty': 12.0, 'price': 102.0, 'amt': 1224.0}, {'line_id': 2, 'item_id': 8759, 'item_subno': '8004385033310', 'item_name': '天使之手干红葡萄酒', 'unit_no': '瓶', 'pack_qty': 100.0, 'unit_qty': 1.0, 'qty': 100.0, 'price': 71.0, 'amt': 7100.0}], 'brs': [{'line_id': 1, 'item_id': 6386, 'brh_no': '0001', 'qty': 6.0}, {'line_id': 2, 'item_id': 6386, 'brh_no': '0002', 'qty': 6.0}, {'line_id': 3, 'item_id': 8759, 'brh_no': '0001', 'qty': 50.0}, {'line_id': 4, 'item_id': 8759, 'brh_no': '0002', 'qty': 50.0}]}]
        }

    """

    """
        @api {put}  /api/inout/ro/<string:sheet_no>  修改处理标志
        @apiVersion 1.0.0
        @apiName  UpdateReturnOut
        @apiGroup 采购退货单

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
    sheet_type = SheetType.ro.value


class InoutQSApi(InoutApi):
    """
        @api {get}  /api/inout/qs/<string:sheet_no>   获取单据信息
        @apiVersion 1.0.0
        @apiName  Sale
        @apiGroup 商品销售

        @apiPermission supply
        @apiUse  AuthRequired
        @apiUse GetSheet
        @apiUse ErrorExample
        @apiUse InoutReturnParam

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200
        {
            [{'sheet_no': '18091700DO0130', 'sheet_type': 'DO', 'sup_no': '203701', 'sup_name': '湖北致远天下贸易有限公司', 'brh_no': '9999', 'brh_name': '中百好邦干货物流仓', 'po_brh_no': '', 'sum_amt': 8324.0, 'deliver_date': '2018-09-20', 'valid_date': '2018-09-21', 'cr_date': '2018-09-17', 'cr_time': '15:41:36', 'status': '5', 'cr_oper_no': '0122', 'details': [{'line_id': 1, 'item_id': 6386, 'item_subno': '3211203450258', 'item_name': 'CASTEL卡柏莱美乐干红（木盒）750ml', 'unit_no': '瓶', 'pack_qty': 12.0, 'unit_qty': 1.0, 'qty': 12.0, 'price': 102.0, 'amt': 1224.0}, {'line_id': 2, 'item_id': 8759, 'item_subno': '8004385033310', 'item_name': '天使之手干红葡萄酒', 'unit_no': '瓶', 'pack_qty': 100.0, 'unit_qty': 1.0, 'qty': 100.0, 'price': 71.0, 'amt': 7100.0}], 'brs': [{'line_id': 1, 'item_id': 6386, 'brh_no': '0001', 'qty': 6.0}, {'line_id': 2, 'item_id': 6386, 'brh_no': '0002', 'qty': 6.0}, {'line_id': 3, 'item_id': 8759, 'brh_no': '0001', 'qty': 50.0}, {'line_id': 4, 'item_id': 8759, 'brh_no': '0002', 'qty': 50.0}]}]
        }

    """

    """
        @api {put}  /api/inout/qs/<string:sheet_no>  修改处理标志
        @apiVersion 1.0.0
        @apiName  UpdateSale
        @apiGroup 商品销售

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
    sheet_type = SheetType.qs.value


class InoutQTApi(InoutApi):
    """
        @api {get}  /api/inout/qt/<string:sheet_no>   获取单据信息
        @apiVersion 1.0.0
        @apiName  ReturnSale
        @apiGroup 商品销售退货

        @apiPermission supply
        @apiUse  AuthRequired
        @apiUse GetSheet
        @apiUse ErrorExample
        @apiUse InoutReturnParam

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200
        {
            [{'sheet_no': '18091700DO0130', 'sheet_type': 'DO', 'sup_no': '203701', 'sup_name': '湖北致远天下贸易有限公司', 'brh_no': '9999', 'brh_name': '中百好邦干货物流仓', 'po_brh_no': '', 'sum_amt': 8324.0, 'deliver_date': '2018-09-20', 'valid_date': '2018-09-21', 'cr_date': '2018-09-17', 'cr_time': '15:41:36', 'status': '5', 'cr_oper_no': '0122', 'details': [{'line_id': 1, 'item_id': 6386, 'item_subno': '3211203450258', 'item_name': 'CASTEL卡柏莱美乐干红（木盒）750ml', 'unit_no': '瓶', 'pack_qty': 12.0, 'unit_qty': 1.0, 'qty': 12.0, 'price': 102.0, 'amt': 1224.0}, {'line_id': 2, 'item_id': 8759, 'item_subno': '8004385033310', 'item_name': '天使之手干红葡萄酒', 'unit_no': '瓶', 'pack_qty': 100.0, 'unit_qty': 1.0, 'qty': 100.0, 'price': 71.0, 'amt': 7100.0}], 'brs': [{'line_id': 1, 'item_id': 6386, 'brh_no': '0001', 'qty': 6.0}, {'line_id': 2, 'item_id': 6386, 'brh_no': '0002', 'qty': 6.0}, {'line_id': 3, 'item_id': 8759, 'brh_no': '0001', 'qty': 50.0}, {'line_id': 4, 'item_id': 8759, 'brh_no': '0002', 'qty': 50.0}]}]
        }

    """

    """
        @api {put}  /api/inout/qt/<string:sheet_no>  修改处理标志
        @apiVersion 1.0.0
        @apiName  UpdateReturnSale
        @apiGroup 商品销售退货

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
    sheet_type = SheetType.qt.value
