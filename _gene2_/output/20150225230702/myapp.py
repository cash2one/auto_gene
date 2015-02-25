#encoding:utf8
from flask import Flask

import etc as config

app = Flask(__name__)

from controller.admin import *


if __name__ == "__main__":
    app.debug = config.debug_mode 
    app.secret_key = config.session_key
    app.run()