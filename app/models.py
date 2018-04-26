from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class Userval(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	d1 = db.Column(db.Integer, index=True, unique=True)
	d2 = db.Column(db.Integer, index=True, unique=True)
	d3 = db.Column(db.Integer, index=True, unique=True)
	d4 = db.Column(db.Integer, index=True, unique=True)
	d5 = db.Column(db.Integer, index=True, unique=True)
	d6 = db.Column(db.Integer, index=True, unique=True)
	
	on_off = db.Column(db.Integer, index=True, unique=True)
	#freq = db.Column(db.Integer, index=True, unique=True)
	#amp = db.Column(db.Integer, index=True, unique=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Duty Cycle 1 {}>'.format(self.d1) #.format(self.amp)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	values = db.relationship('Userval', backref='val', lazy='dynamic')
	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	
	def __repr__(self):
		return '<User {}>'.format(self.username)
		

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# STARTING DATABASE FROM SCRATCH
# python -m flask db init
# python -m flask db migrate -m "table"				#add esdhfl;a234_table file to version inside migrations dir
# python -m flask db upgrade 							#creates app.db

# Try deleting the old app.db file and using flask db migrate