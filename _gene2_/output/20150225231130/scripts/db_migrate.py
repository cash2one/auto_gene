#encoding:utf8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

import os
import sys
sys.path.append (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.model_cms import app,db
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    #command python aaa.py db init | migrate | upgrade
    manager.run()