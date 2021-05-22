import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False # for warning suppression


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir, "dev-db.sqlite")


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

