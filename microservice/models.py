from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class BrDynamic(db.Model):
    __tablename__ = "t_br_dynamic"
    brhno = db.Column('fbrh_no', db.String(),primary_key=True)
    dynamicgrp = db.Column("fdynamic_grp", db.String())

    def get_grpno(self, brhno):
        return self.query.get(brhno).dynamicgrp


class Supply(db.Model):
    """供应商"""
    __tablename__ = 't_bs_master'
    supno = db.Column("fsup_no", db.String(), primary_key=True)
    supname = db.Column('fsup_name', db.String())



class Branch(db.Model):
    """门店"""
    __tablename__ = 't_br_master'
    brhno = db.Column("fbrh_no", db.String(), primary_key=True)
    brhname = db.Column("fbrh_name", db.String())


class Item(db.Model):
    """商品"""
    __tablename__ = 't_bi_master'
    itemid = db.Column("fitem_id", db.Integer,primary_key=True)
    itemno = db.Column("fitem_no",db.String, unique=True)
    itemsubno = db.Column("fitem_subno", db.String, unique=True)
    itemname = db.Column("fitem_name", db.String)


class OrderMaster(db.Model):
    """订单"""
    __tablename__ = 't_order_master'

    sheetno = db.Column("fsheet_no", db.String(14), primary_key=True)
    sheettype = db.Column("fsheet_type", db.String(2))
    supno = db.Column("fsup_no", db.String(6), db.ForeignKey("t_bs_master.fsup_no"))
    brhno = db.Column("fbrh_no", db.String(6), db.ForeignKey('t_br_master.fbrh_no'))
    pobrhno = db.Column("fpo_brh_no", db.String(6))
    sumamt = db.Column("fsum_amt", db.Float())
    deliverdate = db.Column("fdeliver_date", db.Date())
    validdate = db.Column("fvalid_date", db.Date())
    crdate = db.Column("fcr_date", db.Date())
    crtime = db.Column('fcr_time',db.Time())
    status = db.Column("fstatus", db.String(1))
    croperno = db.Column('fcr_oper_no', db.String(6))
    webapiflag = db.Column('fwebapi_flag', db.String(1))

    details = db.relationship('OrderDetail', backref="master")
    brs = db.relationship('OrderBr', backref="master")
    supply = db.relationship("Supply", foreign_keys=[supno], uselist=False)
    branch = db.relationship("Branch", foreign_keys=[brhno], uselist=False)


class OrderDetail(db.Model):
    """订单明细"""
    __tablename__ = 't_order_detail'

    sheetno = db.Column('fsheet_no', db.String(), db.ForeignKey("t_order_master.fsheet_no"), primary_key=True )
    lineid = db.Column('fline_id', db.Integer(), primary_key=True)
    itemid = db.Column("fitem_id",db.Integer(),db.ForeignKey("t_bi_master.fitem_id"))
    itemsubno = db.Column("fitem_subno", db.String())
    unitno = db.Column('funit_no', db.String(4))
    unitqty = db.Column('funit_qty', db.Numeric(19, 3))
    packqty = db.Column('fpack_qty', db.Numeric(19, 3))
    qty = db.Column("fqty", db.Numeric(19, 3))
    price = db.Column("fprice", db.Numeric(19, 4))
    amt = db.Column('famt', db.Numeric(19, 2))
    giveflag = db.Column('fgive_flag', db.String(1))
    promoteflag = db.Column('fpromote_flag', db.String(1))

    item = db.relationship("Item", foreign_keys=[itemid], uselist=False)


class OrderBr(db.Model):
    """订单门店"""
    __tablename__ = 't_order_br'
    sheetno = db.Column('fsheet_no', db.String(), db.ForeignKey("t_order_master.fsheet_no"), primary_key=True)
    lineid = db.Column('fline_id', db.Integer(), primary_key=True)
    itemid = db.Column("fitem_id", db.Integer())
    brhno = db.Column("fbrh_no", db.String(6))
    qty = db.Column('fqty', db.Numeric(19, 3))


class DynamicModel:
    """分组表"""
    _mapper = {}     # 缓存model名和对象映射关系
    table_name = ''  # 主表名
    columns = {}     # model列
    table_index = ""

    def __init__(self, grpno=None, brhno=None):
        self.grpno = grpno
        self.brhno = brhno
        self.table_index = self.get_table_index()

    def get_table_index(self):
        """获取表名索引"""
        if self.brhno and not self.grpno:  # 如果传入分组名，则直接以分组名
            table_index = '_' + BrDynamic().get_grpno(self.brhno)
        elif self.grpno:
            table_index = '_' + self.grpno
        else:
            table_index = ""
        return table_index

    def model(self):
        # 如果传入分组标号，则直接取分组标号
        class_name = '{}{}'.format(self.table_name, self.table_index)
        model_class = self._mapper.get(class_name, None)

        model_column = {
            '__module__': __name__,
            '__name__': class_name,
            '__tablename__': '{}{}'.format(self.table_name, self.table_index),
        }

        #  model列
        model_column.update(self.columns)

        if model_class is None:
            model_class = type(class_name, (db.Model,), model_column)
            self._mapper[class_name] = model_class

        cls = model_class()
        return cls.__class__


class DynamicInoutDetail(DynamicModel):

    table_name = 't_inout_detail'

    def __init__(self, brhno=None, grpno=None):
        super(__class__).__init__()
        self.brhno = brhno
        self.grpno = grpno
        self.table_index = self.get_table_index()
        self.columns = {
            'sheetno': db.Column('fsheet_no',
                                 db.String(), db.ForeignKey("t_inout_master{}.fsheet_no".format(self.table_index)),
                                 primary_key=True),
            'lineid': db.Column('fline_id', db.Integer, primary_key=True),
            'itemid': db.Column("fitem_id", db.Integer),
            'itemsubno': db.Column("fitem_subno", db.String(25)),
            'unitno': db.Column('funit_no', db.String(4)),
            'unitqty': db.Column('funit_qty', db.Numeric(19, 3)),
            'packqty': db.Column('fpack_qty', db.Numeric(19, 3)),
            'qty': db.Column("fqty", db.Numeric(19, 3)),
            'price': db.Column("fprice", db.Numeric(19, 4)),
            'amt': db.Column('famt', db.Numeric(19, 2)),
        }


class DynamicInoutMaster(DynamicModel):

        table_name = 't_inout_master'

        def __init__(self, brhno=None,grpno=None):
            super(__class__).__init__()
            self.brhno = brhno
            self.grpno = grpno
            self.table_index = self.get_table_index()
            dynamicinoutdetail = DynamicInoutDetail(grpno=grpno, brhno=brhno)
            Detail = dynamicinoutdetail.model()
            self.columns = {
                'sheetno': db.Column("fsheet_no", db.String(14), primary_key=True),
                'sheettype': db.Column("fsheet_type", db.String(2)),
                'status': db.Column('fstatus', db.String(1)),
                'srctype': db.Column('fsrc_type', db.String(1)),
                'srcno': db.Column('fsrc_no', db.String(14)),
                'supno': db.Column('fsup_no', db.String(8)),
                'brhno': db.Column('fbrh_no', db.String(6)),
                'whno': db.Column('fwh_no', db.String(2)),
                'dbrhno': db.Column('fd_brh_no', db.String(6)),
                'inoutflag': db.Column('finout_flag', db.String(1)),
                'croperno': db.Column('fcr_oper_no', db.String(6)),
                'crdate': db.Column('fcr_date', db.Date),
                'crtime': db.Column('fcr_time', db.Time),
                'sumamt': db.Column('fsum_amt', db.Numeric(19, 2)),
                'webapi': db.Column('fwebapi_flag', db.String(1)),
                'details': db.relationship(Detail),
            }


class DynamicStock(DynamicModel):
    table_name = 't_sk_master'

    def __init__(self, brhno=None, grpno=None):
        super(__class__).__init__()
        self.brhno = brhno
        self.grpno = grpno
        self.table_index = self.get_table_index()

        self.columns = {
            "sheetno": db.Column("fsheet_no", db.String, primary_key=True),
            "lineid": db.Column("fline_id", db.Integer, primary_key=True),
            "brhno": db.Column("fbrh_no", db.String),
            "whno": db.Column('fwh_no', db.String),
            "itemid": db.Column('fitem_id', db.Integer),
            "qty": db.Column("fqty", db.Numeric(19, 3))
        }











