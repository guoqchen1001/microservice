from flask_restful import fields


class OrderFields:
    orderdetail = {
        "lineid": fields.Integer,
        "itemid": fields.Integer,
        "itemsubno": fields.String,
        "itemname": fields.String,
        "unitno": fields.String,
        "packqty": fields.Float,
        "unitqty": fields.Float,
        "qty": fields.Float,
        "price": fields.Float,
        "amt": fields.Float
    }

    orderbr = {
        "lineid": fields.Integer,
        "itemid": fields.Integer,
        "brhno": fields.String,
        "qty": fields.Float
    }

    order = {
        "sheetno": fields.String,
        "sheettype": fields.String,
        "supno": fields.String,
        "supname": fields.String,
        "brhno": fields.String,
        "brhname": fields.String,
        "pobrhno": fields.String,
        "sumamt": fields.Float,
        "deliverdate": fields.String,
        "validdate": fields.String,
        "crdate": fields.String,
        "crtime": fields.String,
        "status": fields.String,
        "croperno": fields.String,
        "details": fields.Nested(orderdetail),
        "brs": fields.Nested(orderbr),
    }


class InoutFields:

    inoutdetail = {
        "lineid": fields.Integer,
        "itemid": fields.Integer,
        "itemsubno": fields.String,
        "itemname": fields.String,
        "unitno": fields.String,
        "packqty": fields.Float,
        "unitqty": fields.Float,
        "qty": fields.Float,
        "price": fields.Float,
        "amt": fields.Float
    }

    inoutmaster = {
        "sheetno": fields.String,
        "sheettype": fields.String,
        "supno": fields.String,
        "supname": fields.String,
        "brhno": fields.String,
        "brhname": fields.String,
        'dbrhno': fields.String,
        'dbrhname':fields.String,
        "sumamt": fields.Float,
        "crdate": fields.String,
        "crtime": fields.String,
        "status": fields.String,
        "croperno": fields.String,
        "details": fields.Nested(inoutdetail),

    }


