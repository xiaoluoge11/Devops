#!/usr/bin/env python
# coding:utf-8

import os
from app import create_app, db
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app.models import switch_pirpost

app = create_app(os.getenv('FLASK_CONFIG') or 'development')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, switch_pirpost=switch_pirpost)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
