import os

basedir = os.path.abspath(os.path.dirname("config.py"))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'kradja'
	print(basedir)

	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db') #I don't think I need the sqlite:///
	SQLALCHEMY_TRACK_MODIFICATIONS = False