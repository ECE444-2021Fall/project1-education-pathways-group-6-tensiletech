import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'cbewhicbeiwcbeiw' # os.environ.get('SECRET_KEY')
    # To mention a relative path, use 3 slashes, relative path is with respect to the root folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' # os.environ.get('SQLALCHEMY_DATABASE_URI')
    ES_CLOUD_ID = "BetterPathTrail:bm9ydGhhbWVyaWNhLW5vcnRoZWFzdDEuZ2NwLmVsYXN0aWMtY2xvdWQuY29tJGJlNjk2ZDk0YTkwMjRjZTFiNDliNWI4MDAwODY1YzY2JGFhNjU1MGMyNDk4ODRmOGFhNDc3MWVmMDVlZGExNDQ3"
    ES_API_KEY = "lYUfA30B_OYIn8plths8"
    ES_API_KEY_SECRET = "GyrgQgcFTEa-1oIAK4eH3A"
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Configuration needed specifically for development

    Args:
        Config (Config Object): Configuring Object for Development
    """
    pass

class TestingConfig(Config):
    """Configuration needed specifically for testing

    Args:
        Config (Config Object): Configuring Object for Testing
    """
    pass

class ProductionConfig(Config):
    """Configuration needed specifically for production

    Args:
        Config (Config Object): Configuring Object for production
    """
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}