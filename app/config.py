class Config:
    SECRET_KEY = "dev-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///bcwd.db"
    UPLOAD_FOLDER = r'E:/bcwd/uploads'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB limit

class DevelopmentConfig(Config):
    DEBUG = True
