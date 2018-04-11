from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from Flask_Question import app
from exts import db
from models import User,Question,Answer

migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()