from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig


app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)


class Order(db.Model):
    """订单"""
    __tablename__ = 't_order_master'

    sheetno = db.Column("fsheet_no", db.String(14), primary_key=True)
    sheettype = db.Column("fsheet_type", db.String(2))
    FsupNo = db.Column("fsup_no",db.String(6))
    brhno = db.Column("fbrh_no", db.String(6))
    pobrhno = db.Column("fpo_brh_no", db.String(6))
    sumamt = db.Column("fsum_amt", db.Float())
    deliverdate = db.Column("fdeliver_date", db.Date())
    validdate = db.Column("fvalid_date", db.Date())
    crdate = db.Column("fcr_date", db.Date())
    crtime = db.Column('fcr_time',db.Time())
    status = db.Column("fstatus", db.String(1))
    croperno = db.Column('fcr_oper_no', db.String(6))

    details = db.relationship(
        'OrderDetail',
        backref='master',
        lazy='dynamic'
    )
    brs = db.relationship(
        'OrderBr',
        backref='master',
        lazy='dynamic'
    )

    supply = db.relationship(
        "Supply",
        lazy='select',
        uselist=False
    )

class OrderDetail(db.Model):
    """订单明细"""
    __tablename__ = 't_order_detail'

    sheetno = db.Column('fsheet_no',db.String(), db.ForeignKey("t_order_master.fsheet_no"),primary_key=True )
    lineid = db.Column('fline_id', db.Integer(), primary_key=True)
    itemid = db.Column("fitem_id",db.Integer())
    itemsubno = db.Column("fitem_subno", db.String())
    unitno = db.Column('funit_no', db.String())
    unitqty = db.Column('funit_qty', db.Numeric(19, 3))
    packqty = db.Column('fpack_qty', db.Numeric(19, 3))
    price = db.Column("fprice", db.Numeric(19, 4))
    amt = db.Column('famt', db.Numeric(19, 2))
    giveflag = db.Column('fgive_flag', db.String(1))
    promoteflag = db.Column('fpromote_flag', db.String(1))


class OrderBr(db.Model):
    """订单门店"""
    __tablename__ = 't_order_br'
    sheetno = db.Column('fsheet_no', db.String(), db.ForeignKey("t_order_master.fsheet_no"), primary_key=True)
    lineid = db.Column('fline_id', db.Integer(), primary_key=True)
    itemid = db.Column("fitem_id", db.Integer())
    brhno = db.Column("fbrh_no", db.String(6))
    qty = db.Column('fqty', db.Numeric(19,3))

class Supply(db.Model):
    """供应商"""
    __tablename__ = 't_bs_master'
    supno = db.Column("fsup_no", db.String(), db.ForeignKey("t_order_master.fsup_no"),primary_key=True)
    supname = db.Column('fsup_name', db.String())

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    order = Order.query.all()
    print(order)

    app.run()
