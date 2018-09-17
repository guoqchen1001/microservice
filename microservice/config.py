from .extensions import DecimalEncoder


class Config:
    RESTFUL_JSON = dict(ensure_ascii=False, cls=DecimalEncoder)
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 该参数下个版本会被设成默认
    TOKEN_EXPIRES_IN = 600  # token过期时间


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mssql+pymssql://sa:123@127.0.0.1:1433/zbhb?charset=utf8"  # 数据库链接地址
    SECRET_KEY = '@kmtech2018@'  # token密钥
    TOKEN_EXPIRES_IN = 86400  # token过期时间
