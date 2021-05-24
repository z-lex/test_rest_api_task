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


def get_config(config_name):
    """
    get config class by its name string
    :param config_name:
    :return: config class
    """
    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
    }
    return configs.get(config_name, DevelopmentConfig)
