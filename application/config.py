class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class LocalDevelopmentConfig(Config):

    #configs of database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lmsv2.sqlite3'
    DEBUG = True

    #configs of flask-security
    SECRET_KEY = 'this-really-needs-to-be-changed' # hash user credentials in session
    SECURITY_PASSWORD_HASH = "bcrypt" # mechanism for password hashing
    SECURITY_PASSWORD_SALT = "password-salt" # helps in password hashing
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "X-Auth-Token"