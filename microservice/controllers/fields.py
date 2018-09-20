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

    inoutmaster = {
        "sheet_no": fields.String,
        "sheet_type": fields.String,
        "src_no": fields.String,
        "sup_no": fields.String,
        "sup_name": fields.String,
        "brh_no": fields.String,
        "brh_name": fields.String,
        'd_brh_no': fields.String,
        'd_brh_name':fields.String,
        "sum_amt": fields.Float,
        "cr_date": fields.String,
        "cr_time": fields.String,
        "status": fields.String,
        "cr_oper_no": fields.String,
        "details": fields.Nested(inoutdetail),

    }


class StockFields:
    stock = {
        "brh_no": fields.String,
        "brh_name": fields.String,
        "wh_no": fields.String,
        "wh_name": fields.String,
        "item_id": fields.Integer,
        "item_no": fields.String,
        "item_subno": fields.String,
        "item_name": fields.String,
        "qty": fields.Float
    }


