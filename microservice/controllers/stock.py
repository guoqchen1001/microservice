from flask_restful import Resource, abort, marshal_with
from sqlalchemy import and_
from .base import SheetBase
from ..models import DynamicStock, Branch, Item, BranchWareHouse, BrDynamic
from .. import db
from .parsers import StockParser
from .fields import StockFields
from .auth import AuthApi


class StockApi(Resource):
    """库存接口"""
    perpage = SheetBase.per_page
    br_dynamic = None

    @AuthApi.auth_required
    @marshal_with(StockFields.stock)
    def get(self, brh_no=None, user=None):
         """
        @api {get}  /api/stock/<string:brh_no>  获取库存信息
        @apiVersion 1.0.0
        @apiName  GetStock
        @apiGroup 库存查询

        @apiPermission supply
        @apiUse  AuthRequired
        @apiParam (入参) {string} page 页数
        @apiUse ErrorExample
        @apiUse StockSuccessParam

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200
        {
            [
                {
                    "brh_no": "9999",
                    "brh_name": "中百好邦干货物流仓",
                    "wh_no": "01",
                    "wh_name": "正常拣货仓",
                    "item_id": 469,
                    "item_no": "100474",
                    "item_subno": "3182520195965",
                    "item_name": "尼罗莉红葡萄酒750ml",
                    "qty": 6
                },
                {
                    "brh_no": "9999",
                    "brh_name": "中百好邦干货物流仓",
                    "wh_no": "01",
                    "wh_name": "正常拣货仓",
                    "item_id": 499,
                    "item_no": "100496",
                    "item_subno": "4054500133818",
                    "item_name": "凯尔特人小麦啤酒500ml",
                    "qty": 145
                },

        }

    """

        # 获取登录人员有权限的供应商
        sup_no = user.get_supply()

        args = StockParser.get.parse_args()
        page = args['page'] or 1

        if brh_no:
            # 创建动态对象
            Stock = DynamicStock(brh_no=brh_no).model()
            # 检索数据
            result = db.session.query(
                Stock.brh_no.label("brh_no"),
                Stock.wh_no.label("wh_no"),
                Stock.item_id.label("item_id"),
                db.func.sum(Stock.qty).label("qty")).filter(
                Stock.brh_no == brh_no,
                Stock.sup_no.in_(sup_no)).group_by(
                Stock.brh_no, Stock.wh_no, Stock.item_id).order_by(
                Stock.brh_no, Stock.item_id).limit(
                self.perpage*page).offset(self.perpage*(page-1)).subquery("t1")

            # 获取商品名称等信息
            result = db.session.query(result,
                                      Branch.brh_name,
                                      Item.item_no,
                                      Item.item_name,
                                      Item.item_subno,
                                      BranchWareHouse.wh_name).outerjoin(
                Branch, result.c.brh_no == Branch.brh_no).outerjoin(
                Item, result.c.item_id == Item.item_id).outerjoin(
                BranchWareHouse, and_(
                    result.c.brh_no == BranchWareHouse.brh_no,
                    result.c.wh_no == BranchWareHouse.wh_no
                ))

            # 重新构造数据，转换为dict
            columns_name = [desc["name"] for desc in result.column_descriptions]
            result = [dict(zip(columns_name, value)) for value in result.all()]
            return result
        else:
            if not self.br_dynamic:
                br_dynamic_list = db.session.query(BrDynamic.dynamic_grp).distinct().all()

                stock_all = []
                for br_dynamic in br_dynamic_list:
                    Stock = DynamicStock(grp_no=br_dynamic.dynamic_grp).model()
                    # 检索数据
                    result = db.session.query(
                        Stock.brh_no.label("brh_no"),
                        Stock.wh_no.label("wh_no"),
                        Stock.item_id.label("item_id"),
                        db.func.sum(Stock.qty).label("qty")).filter(
                        Stock.sup_no.in_(sup_no)).group_by(
                        Stock.brh_no, Stock.wh_no, Stock.item_id).order_by(
                        Stock.brh_no, Stock.item_id).limit(
                        self.perpage*page).subquery("t1")

                    # 获取商品名称等信息
                    result = db.session.query(result,
                                              Branch.brh_name,
                                              Item.item_no,
                                              Item.item_name,
                                              Item.item_subno,
                                              BranchWareHouse.wh_name).outerjoin(
                        Branch, result.c.brh_no == Branch.brh_no).outerjoin(
                        Item, result.c.item_id == Item.item_id).outerjoin(
                        BranchWareHouse, and_(
                            result.c.brh_no == BranchWareHouse.brh_no,
                            result.c.wh_no == BranchWareHouse.wh_no
                        ))

                    columns_name = [desc["name"] for desc in result.column_descriptions]
                    result = [dict(zip(columns_name, value)) for value in result.all()]

                    stock_all.extend(result)

                return stock_all[(page-1)*self.perpage: page*self.perpage]












