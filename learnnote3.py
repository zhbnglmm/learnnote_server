from flask import Flask, request
import sys
import os
try:
    import config_override as config
except ImportError:
    import config_default as config
from exts import db
from models import Label, LearnNote, FileNumber, Picture
import logging
import json
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)




app.debug = True
handler = logging.FileHandler(config.LOG_FILE_FULL_PATH, encoding='UTF-8')
handler.setLevel(logging.DEBUG)
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
    pass