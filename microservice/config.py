class Config:
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mssql+pymssql://sa:123@127.0.0.1:1433/zbhb"
