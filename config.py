class Config(object):
    DEBUG = True
    SECRET_KEY = "mysecretkey"
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:postgres@localhost:5432/postgres"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI="sqlite://"