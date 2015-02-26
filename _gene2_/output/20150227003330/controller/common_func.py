#encoding:utf-8
from common_import import *
from common_app_db import *

def md5 (s):
    return hashlib.md5(s).hexdigest()

def tojson (data):
    return json.dumps (data)

def get_parameter (*p):
    result = {}
    for i in p:
        result[i] = request.form.get(i,'')
    return result

def get_site_info ():
    site_info = {}
    return site_info

site = get_site_info()

def default_error (msg):
    return render_template ('admin/default_error.html', msg=msg)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_login' not in session:
            return redirect(config.login_url)
        return f(*args, **kwargs)
    return decorated
from model.model_hr import Staff as db_Staff
from model.model_hr import Department as db_Dept
from model.model_hr import Position as db_Position
from model.model_hr import Salary as db_Salary

from admin_staff import *
from admin_dept import *
from admin_position import *
from admin_salary import *

