class Config:
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mssql+pymssql://sa:123@127.0.0.1:1433/zbhb"  # 数据库链接地址
    JSON_AS_ASCII = False   # json中文处理
    SQLALCHEMY_TRACK_MODIFICATIONS = True
