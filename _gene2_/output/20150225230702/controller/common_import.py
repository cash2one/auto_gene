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

from model.model_cms import db
import etc as config
import tools.common as common
import tools.common_flask as common_flask

from model.model_cms import User as db_User
from model.model_cms import Book as db_Book
from model.model_cms import Author as db_Author
from model.model_cms import Category as db_Category

from myapp import app

from admin_user import *
from admin_book import *
from admin_author import *
from admin_category import *