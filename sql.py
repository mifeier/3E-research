from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import datetime
import hashlib
from conf import GetConfig
from sqlalchemy.orm import aliased
import re

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'role'
    Id=db.Column(db.Integer)
    role_id = db.Column(db.Integer, primary_key=True)
    role_ame = db.Column(db.String(128))

class User(db.Model):
    __tablename__='user'
    Id=db.Column(db.Integer,primary_key=True)
    role_id=db.Column(db.Integer)

class Project(db.Model):
    __tablename__='project'
    Id=db.Column(db.Integer,primary_key=True)
    pro_id=db.Column(db.Integer)
    pro_name=db.Column(db.String(128))
    pro_detail=db.Column(db.String(128))
    page_id=db.Column(db.Integer)
    
class Page(db.Model):
    __tablename__='page'
    Id = db.Column(db.Integer,primary_key=True)
    page_id=db.Column(db.Integer)
    page_name=db.Column(db.String(128))
    page_detail=db.Column(db.String(128))
    func_id=db.Column(db.Integer)

class Function(db.Model):
    __tablename__='functions'
    Id = db.Column(db.Integer,primary_key=True)
    func_id=db.Column(db.Integer)
    func_name=db.Column(db.String(128))
    func_detail=db.Column(db.Integer)
    designer_id=db.Column(db.Integer)

class Designer(db.Model):
    __tablename__='designer'
    Id = db.Column(db.Integer,primary_key=True)
    designer_id=db.Column(db.Integer)
    content=db.Column(db.String(128))
    role_id=db.Column(db.Integer)

    


