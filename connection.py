from flask import Flask


from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
import hashlib
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from flask import session as login_session

import httplib2
import requests
import json




app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/Ofaly'

db = SQLAlchemy(app)

class users(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   fb_id = db.Column(db.Integer)
   name = db.Column(db.String(100))  
   picture = db.Column(db.String(512))


   def __init__(self, name=None, fb_id=None, picture=None):
        self.name = name
        self.fb_id = fb_id
        self.picture = picture



class posts(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   fb_id = db.Column(db.Integer)
   message = db.Column(db.String(512))
   createdTime = db.Column(db.String(70))


   def __init__(self, fb_id=None ,message=None ,createdTime=None) :

        self.fb_id = fb_id
        self.message = message
        self.createdTime = createdTime




