# encoding : utf-8
import os

DEBUG = True
USERNAME = "root"
PASSWORD = "root"
HOST = "127.0.0.1"
DATABASE = "learnnote3"
SECRET_KEY = os.urandom(24)
LOG_FILE_FULL_PATH = "C:\\Alan\\learnnote3\\flasklog.log"
DIALECT = "mysql"
DRIVER = "pymysql"
PORT = "3306"
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
