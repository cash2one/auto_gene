# encoding:utf8

import json
import hashlib

from flask import Flask
from flask import flash
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import make_response
from flask import render_template
from flask import get_flashed_messages

from werkzeug import secure_filename
from functools import wraps

from sqlalchemy import or_, and_

import os
import sys
sys.path.append (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import etc as config
import tools.common as common
import tools.common_flask as common_flask

from common_app_db import app
from common_app_db import db
