import json
import decimal


class DecimalEncoder(json.JSONEncoder):
    """重新定义json解析"""
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, bytes):
            return o.decode(encoding='utf-8')
        return super(DecimalEncoder, self).default(o)


class Config:
    RESTFUL_JSON = dict(ensure_ascii=False, cls=DecimalEncoder)
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mssql+pymssql://sa:123@127.0.0.1:1433/zbhb?charset=utf8"  # 数据库链接地址
    SECRET_KEY = 'kmtech2018'
