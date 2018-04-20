import datetime
from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from app.forms import RegistrationForm, InputForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User, Userval

#global temp_freq
#global temp_amp

temp_freq = 0
temp_amp = 0 
#app = Flask(__name__)
#app.config['SECRET_KEY'] = 'kradja'
@app.route("/", methods=('GET', 'POST'))
@app.route("/index", methods=('GET', 'POST'))
@login_required
def index():
	print('hello')
	#form = InputForm(request.form)
	
	#if request.method == 'POST': # Validator to verify that the input fulfills some criteron.
	#	freq=request.form['frequency']
	#	print(freq)
	
	form = InputForm()

	cuserval = Userval.query.get(current_user.id)
	print(cuserval)
	if form.validate_on_submit():
		print(form.frequency.data)
		cuserval.freq = form.frequency.data
		cuserval.amp = form.amplitude.data
		print(cuserval.freq)
		print(cuserval.amp)
		db.session.commit()
		get_tasks()
	
	current_time = datetime.datetime.utcnow()
	previous_time = current_time - datetime.timedelta(days = 1,seconds = 2, hours = 5)
	previous_time2 = current_time - datetime.timedelta(days = 4,seconds = 5, hours = 1)
	
	listofuses = [
	{
		'user' : {'username' : 'Kevin'},
		'time' : previous_time.strftime('%m/%d/%Y')
	},
	{
		'user' : {'username' : 'Gerrit'},
		'time' : previous_time2.strftime('%m/%d/%Y')
	}]
	
	#frequencyval = request.form.get("freq_num","")
	
	
	return render_template('index.html', title = 'Home', ulist = listofuses, cuserval = cuserval,form = form)#, frequencyval = frequencyval)

@app.route("/login", methods=('GET', 'POST'))
def login():
	
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	form = LoginForm()
	
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			
			return redirect(url_for('login'))
		
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('index'))	
	
	return render_template('login.html', title = 'Sign In',form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data)
		user.set_password(form.password.data)
		db.session.add(user)
		
		userval = Userval(freq=0,amp=0)
		db.session.add(userval)
		db.session.commit()
		flash('You are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)
	

@app.route('/api/data', methods=['GET'])
def get_tasks():
	global temp_freq
	global temp_amp
	print('HELLO')
	print(request.remote_addr)
	if current_user.is_authenticated:
		#temp = current_user.id
		cuserval = Userval.query.get(current_user.id)
		temp_freq = cuserval.freq
		temp_amp = cuserval.amp
		return jsonify({'Frequency': temp_freq, 'Amplitude': temp_amp})
	return jsonify({'Frequency': temp_freq, 'Amplitude': temp_amp})
	#else:
	#	cuserval = Userval.query.get(temp)
		
	#else:
	#	return jsonify({'Frequency': cuserval.freq, 'Amplitude': cuserval.amp})	
	
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
	
#if __name__ == "__main__":
#	app.run(host='0.0.0.0',port = 8090)
# Keeping the initialization inside routes.py makes this work
