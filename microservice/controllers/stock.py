from flask_restful import Resource, abort, marshal_with
from .base import SheetBase
from ..models import DynamicStock,Branch,Item
from .. import  db
from .parsers import StockParser



class StockApi(Resource):
    """库存接口"""
    perpage = SheetBase.per_page

    def get(self, brhno=None):
        """get方法"""
        if not brhno:
            abort(400, message="无效的门店编码")
        else:
            args = StockParser.get.parse_args()
            page = args['page'] or 1

            Stock = DynamicStock(brhno=brhno).model()
            result = db.session.query(
                Stock.brhno, Branch.brhname, Stock.whno, Item.itemno, Item.itemsubno, Item.itemname,
                db.func.sum(Stock.qty) ).outerjoin(
                Branch, Stock.brhno == Branch.brhno).outerjoin(
                Item, Stock.itemid == Item.itemid).filter(
                Stock.brhno == brhno).group_by(
                Stock.brhno, Branch.brhname, Stock.whno, Item.itemno, Item.itemsubno, Item.itemname).order_by(
                Stock.brhno, Item.itemno).limit(
                self.perpage).offset(page - 1).all()


            column_name_list = ('brhno', 'brhname', 'whno', 'itemno', 'itemsubno', 'itemname', 'qty')
            result_json = [dict(zip(column_name_list, r)) for r in result]
            return result_json








