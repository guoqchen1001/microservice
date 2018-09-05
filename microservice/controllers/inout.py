from flask_restful import Resource
from ..models import  InoutMaster, InoutDetail


class InoutApi(Resource):
    """出入库"""
    def get(self,sheetno=None):
        if sheetno:
            grpno = sheetno[5:6]
            Inout = InoutMaster.model(grpno=grpno)
            inout = Inout.query.get(sheetno)
            if not inout:
                abort(404, "单号{}不存在".format(sheetno))
            return inout
        else:
            pass


