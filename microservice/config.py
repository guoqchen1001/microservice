class Config:
    JSON_AS_ASCII = False   # json中文处理
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(Config):
    pass


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mssql+pymssql://sa:123@127.0.0.1:1433/zbhb?charset=utf8"  # 数据库链接地址
    DEBUG = True
    SQLALCHEMY_ECHO = False

