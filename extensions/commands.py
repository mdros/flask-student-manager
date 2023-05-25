from models import Student

from .database import db


def create_db():
    print("Creating db...")
    db.create_all()


def drop_db():
    print("Dropping db...")
    db.drop_all()


def init_app(app):
    for command in [create_db, drop_db]:
        app.cli.add_command(app.cli.command()(command))
