import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config(object):
    """Parent configuration class."""
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://rohan:rohan@localhost/bardog' #'sqlite:///' + os.path.join(basedir, 'app.sqlite')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://rohan:rohan@localhost/testing' #'sqlite:///' + os.path.join(basedir, 'test.sqlite')
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Rohan@0870@35.200.96.173/bardog?host=35.200.96.173?port=3306'


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
