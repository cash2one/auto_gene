# encoding:utf8

import os
import sys
sys.path.append (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from myapp import app
from model.model_hr import db