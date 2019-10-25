from datetime import datetime
from  flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Grade(db.Model):
    g_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    g_name = db.Column(db.String(20),unique=True)
    g_create_time = db.Column(db.DateTime,default=datetime.now())
    students = db.relationship('Student',backref='grade')

class Student(db.Model):
    s_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    s_name = db.Column(db.String(16),unique=True)
    s_sex = db.Column(db.Integer)
    grade_id = db.Column(db.Integer,db.ForeignKey('grade.g_id'),nullable=True)

class User(db.Model):
    u_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(16),unique=True)
    password = db.Column(db.String(250))
    u_create_time = db.Column(db.DateTime, default=datetime.now())
    role_id = db.Column(db.Integer,db.ForeignKey('role.r_id'))

class Role(db.Model):
    r_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    r_name = db.Column(db.String(10),unique=True)
    users = db.relationship('User',backref='role')

r_p = db.Table(
                'r_p',
                db.Column('role_id',db.Integer,db.ForeignKey('role.r_id'),primary_key=True),
                db.Column('permission_id',db.Integer,db.ForeignKey('permission.p_id'),primary_key=True)
               )

class Permission(db.Model):
    p_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    p_name = db.Column(db.String(16),unique=True)
    p_er = db.Column(db.String(16),unique=True)
    roles = db.relationship('Role',secondary=r_p,backref=db.backref('permission'))
