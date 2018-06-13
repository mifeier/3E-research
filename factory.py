from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from conf import GetConfig
from sql import db


def create_app(app):
    conf = GetConfig()
    app.config['SQLALCHEMY_DATABASE_URI'] = conf["database"]["connection"]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = conf["database"]["debug"]

    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app