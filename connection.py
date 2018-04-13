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
import tweepy
from tweepy import OAuthHandler





app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/Ofaaly'

db = SQLAlchemy(app)

class users(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   tw_id = db.Column(db.Integer)
   name = db.Column(db.String(100))  
   picture = db.Column(db.String(512))


   def __init__(self, name=None, tw_id=None, picture=None):
        self.name = name
        self.tw_id = tw_id
        self.picture = picture



class posts(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   tw_id = db.Column(db.Integer)
   acc_id = db.Column(db.Integer)
   message = db.Column(db.String(512))
   createdTime = db.Column(db.String(70))


   def __init__(self, acc_id=None, tw_id=None ,message=None ,createdTime=None) :
        self.acc_id = acc_id
        self.tw_id = tw_id.encode('ascii', 'ignore').decode('ascii')
        self.message = message.encode('ascii', 'ignore').decode('ascii')
        self.createdTime = createdTime
   def __repr__(self):
        
        return 'tweet %s %s %s' % (self.message, self.createdTime , self.acc_id)



db.create_all()