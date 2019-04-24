#!/usr/bin/env python
import os
from app import create_app #, db
#from app.models import User, Role
#from flask_script import Manager, Shell
#from flask_migrate import Migrate, MigrateCommand

application = create_app()

if __name__ == '__main__':
    #application.run(host='0.0.0.0', port='8080')
    application.debug= False
    application.run()
