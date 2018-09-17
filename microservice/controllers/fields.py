from flask_restful import fields


class OrderFields:
    orderdetail = {
        "line_id": fields.Integer,
        "item_id": fields.Integer,
        "item_subno": fields.String,
        "item_name": fields.String,
        "unit_no": fields.String,
        "pack_qty": fields.Float,
        "unit_qty": fields.Float,
        "qty": fields.Float,
        "price": fields.Float,
        "amt": fields.Float
    }

    orderbr = {
        "line_id": fields.Integer,
        "item_id": fields.Integer,
        "brh_no": fields.String,
        "qty": fields.Float
    }

    order = {
        "sheet_no": fields.String,
        "sheet_type": fields.String,
        "sup_no": fields.String,
        "sup_name": fields.String,
        "brh_no": fields.String,
        "brh_name": fields.String,
        "po_brh_no": fields.String,
        "sum_amt": fields.Float,
        "deliver_date": fields.String,
        "valid_date": fields.String,
        "cr_date": fields.String,
        "cr_time": fields.String,
        "status": fields.String,
        "cr_oper_no": fields.String,
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
        "srcno": fields.String,
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


class StockFields:
    stock = {
        "brhno": fields.String,
        "brhname": fields.String,
        "whno": fields.String,
        "whname": fields.String,
        "itemid": fields.Integer,
        "itemno": fields.String,
        "itemsubno": fields.String,
        "itemname": fields.String,
        "qty": fields.Float
    }


