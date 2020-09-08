# encoding : utf-8
from exts import db
from datetime import datetime

class Label(db.Model):
    __tablename__ = "tbllabel"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(1000), nullable=False)
    labelcount = db.Column(db.Integer, nullable=False)
    lastusedtime = db.Column(db.DateTime, default=datetime.now)

class LearnNote(db.Model):
    __tablename__ = "tbllearnnote"
    id_problem = db.Column(db.Integer, primary_key=True)
    d_level = db.Column(db.String(100))
    source = db.Column(db.String(100))
    notes = db.Column(db.String(100))
    answer = db.Column(db.String(100))
    usedtime = db.Column(db.DateTime, default=datetime.now)
    usedtimes = db.Column(db.Integer, default=0, nullable=False)
    inputdate = db.Column(db.DateTime, default=datetime.now)
    sync = db.Column(db.Integer, default=0, nullable=False)
    active = db.Column(db.Integer, default=1, nullable=False)

class FileNumber(db.Model):
    __tablename__ = "tblfilenumber"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_problem = db.Column(db.Integer, nullable=False)
    filenumber = db.Column(db.String(100))
    filetitle = db.Column(db.String(100))
    recordtime = db.Column(db.DateTime, default=datetime.now)
    sync = db.Column(db.Integer, default=0, nullable=False)
    active = db.Column(db.Integer, default=1, nullable=False)

class Picture(db.Model):
    __tablename__ = "tblpicture"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_problem = db.Column(db.Integer, db.ForeignKey('tbllearnnote.id_problem'))
    tblpicture = db.relationship("User", backref=db.backref('pictures'))
    filepath = db.Column(db.String(100))
    isanswer = db.Column(db.Integer, default=0, nullable=False)
