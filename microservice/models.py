from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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


class Order(db.Model):
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
    unitno = db.Column('funit_no', db.String())
    unitqty = db.Column('funit_qty', db.Numeric(19, 3))
    packqty = db.Column('fpack_qty', db.Numeric(19, 3))
    qty = db.Column("fqty" ,db.Numeric(19, 3))
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




