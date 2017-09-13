from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager  # class for handling a set of commands

from app import db
from main import app

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
