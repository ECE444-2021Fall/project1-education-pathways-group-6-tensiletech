import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'cbewhicbeiwcbeiw' # os.environ.get('SECRET_KEY')

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