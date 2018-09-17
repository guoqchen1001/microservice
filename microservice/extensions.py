from flask_restful import Api
from flask_apidoc import ApiDoc
import json
import decimal

rest_api = Api()
apidoc = ApiDoc()


class DecimalEncoder(json.JSONEncoder):
    """重新定义json解析"""
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, bytes):
            return o.decode(encoding='utf-8')
        return super(DecimalEncoder, self).default(o)