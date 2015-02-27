#encoding:utf8
from flask import Flask

import etc as config

app = Flask(__name__)

if __name__ == "__main__":
    from controller.admin import *
    
    app.debug = config.debug_mode 
    app.secret_key = config.session_key
    app.run()