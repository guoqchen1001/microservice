from flask_restful import Resource, marshal_with, abort
from ..models import  InoutMaster, Supply, Branch
from .fields import InoutFields
from .. import db


class InoutApi(Resource):
    """出入库"""
    @marshal_with(InoutFields.inoutmaster)
    def get(self,sheetno=None):
        if sheetno:
            grpno = sheetno[6:8]
            Inout = InoutMaster.model(grpno=grpno)
            inout, supply, bracnh = db.session.query(Inout, Supply, Branch).join(
                Supply, Inout.supno == Supply.supno).join(
                Branch, Inout.brhno == Branch.brhno
            ).filter(Inout.sheetno == sheetno).first()

            inout.supname = supply.supname
            inout.brhname = bracnh.brhname
            if not inout:
                abort(404, message="单号{}不存在".format(sheetno))
            return inout
        else:
            pass


