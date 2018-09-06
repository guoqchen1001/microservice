from flask_restful import Resource, marshal_with, abort
from ..models import Supply, Branch, Item,  BrDynamic, DynamicInoutMaster
from .fields import InoutFields
from .. import db
from .parsers import InoutParser
from operator import attrgetter
from .base import SheetStatus, SheetSlice, SheetType, SheetBase


class InoutApi(Resource):
    """出入库"""
    perpage = SheetBase.per_page
    sheettype = ''
    status = SheetStatus.approve.value

    @marshal_with(InoutFields.inoutmaster)
    def get(self, sheetno=None):
        """get方法"""
        args = InoutParser.get.parse_args()
        if not self.sheettype:
            self.sheettype = args['sheettype'] or ''
        if not self.sheettype:
            abort(403, message="单据类型为空")
        if sheetno:
            # 根据单号获取分组表序号
            grpno = sheetno[SheetSlice.sheet_grp_slice]
            Master = DynamicInoutMaster(grpno=grpno).model()
            Dbranch = db.aliased(Branch)
            master, supply, branch, dbranch = db.session.query(Master, Supply, Branch, Dbranch).outerjoin(
                Supply, Master.supno == Supply.supno).outerjoin(
                Branch, Master.brhno == Branch.brhno).outerjoin(
                Dbranch, Master.dbrhno == Dbranch.brhno
            ).filter(Master.sheetno == sheetno,
                     Master.sheettype == self.sheettype).first()

            if not master:
                abort(404, message="单号{}不存在".format(sheetno))
            if supply:
                master.supname = supply.supname
            if branch:
                master.brhname = branch.brhname
            if dbranch:
                master.dbrhname = dbranch.brhname

            details = master.details
            items = Item.query.filter(Item.itemid.in_([detail.itemid for detail in details]))
            for item in items:
                for detail in details:
                    if item.itemid == detail.itemid:
                        detail.itemname = item.itemname

            return master
        else:
            args = InoutParser.get.parse_args()
            page = args['page'] or 1
            brhno = args['brhno'] or ''

            if brhno:
                Master = DynamicInoutMaster(brhno=brhno).model()
                master = Master.query.filter(
                    Master.sheettype == self.sheettype,
                    Master.status == self.status).order_by(
                    Master.crdate.desc(), Master.crtime.desc()).paginate(
                    page, self.perpage)
                return master.items

            else:
                grps = BrDynamic.query.distinct().all()
                grpnos = set([grp.dynamicgrp for grp in grps])
                master_all = []
                for grpno in grpnos:
                    Master = DynamicInoutMaster(grpno=grpno).model()
                    master = Master.query.filter(
                        Master.sheettype == self.sheettype,
                        Master.status == self.status).order_by(
                        Master.crdate.desc(), Master.crtime.desc()).limit(page).all()
                    master_all.extend(master)

                master_all = sorted(master_all, key=attrgetter('crdate','crtime'), reverse=True)
                return master_all[self.perpage*(page - 1):self.perpage*page]

    def put(self, sheetno=None):
        """put方法"""
        if not sheetno:
            abort(400, message="请传入有效的单据号")

        if sheetno:
            grpno = sheetno[SheetSlice.sheet_grp_slice]
            Master = DynamicInoutMaster(grpno=grpno).model()
            master = Master.query.get(sheetno)
            if not master:
                abort(404, message="单号{}不存在".format(sheetno))
            else:
                master.webapiflag = SheetBase.flag_done_yes
                db.session.add(master)
                db.session.commit()

            return master.sheetno


class InoutPIApi(InoutApi):
    """采购收货单"""
    sheettype = SheetType.pi.value


class InoutROApi(InoutApi):
    """采购退货单"""
    sheettype = SheetType.ro.value
    status = SheetStatus.submit.value  # 提交状态



