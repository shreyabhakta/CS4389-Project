#
# class config_production(object):
#
#     DEBUG = False
#     TESTING = False
#     SECRET_KEY = 'a quick brown fox jumps over the lazy dog'
#     ENV = 'production'
#     DEVELOPMENT = False
#
#     MYSQL_DATABASE_USER = 'login'
#     MYSQL_DATABASE_PASSWORD = 'hello123'
#     MYSQL_DATABASE_DB = 'authentication'
#     MYSQL_DATABASE_HOST = 'localhost'
#     TEMPLATES_FOLDER = './'
#     STATIC_FOLDER = "./src"
#
#     GMAIL_USER = "exampleuserjane@gmail.com"
#     GMAIL_PASS = "Merlot123"


class config_development(object):

    DEBUG = True
    TESTING = True
    SECRET_KEY = 'a quick brown fox jumps over the lazy dog'
    DEVELOPMENT = True

    # DB Configs
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = 'trial123456'
    MYSQL_DATABASE_DB = 'authentication'
    MYSQL_DATABASE_HOST = 'localhost'
    TEMPLATES_FOLDER = './'
    STATIC_FOLDER = "./src"

    GMAIL_USER = "exampleuserjane@gmail.com"
    GMAIL_PASS = "Merlot123"
