import os

DEBUG = True
SECRET_KEY = os.urandom(24)
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'flask_question'
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True