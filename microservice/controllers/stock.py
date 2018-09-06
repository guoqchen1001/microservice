from flask_restful import Resource, abort, marshal_with
from .base import SheetBase
from ..models import DynamicStock,Branch,Item
from .fields import StockFields
from .. import  db



class StockApi(Resource):
    perpage = SheetBase.per_page

    @marshal_with(StockFields.stock)
    def get(self, brhno=None):
        """get方法"""
        if not brhno:
            abort(400, message="无效的门店编码")
        else:
            Stock = DynamicStock(brhno=brhno).model()
            result = db.session.query(
                Stock.brhno, Branch.brhno, Branch.brhname, Stock.whno, Item.itemno, Item.itemsubno, Item.itenmae,
                db.func. ).outerjoin(
                Branch, Stock.brhno == Branch.brhno).outerjoin(
                Item, Stock.itemid == Item.itemid).filter(
                Stock.brhno == brhno).all()

            return result









