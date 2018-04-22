import datetime
from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from app.forms import RegistrationForm, InputForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User, Userval

#global temp_freq
#global temp_amp

temp_d1 = 0
temp_d2 = 0 
temp_d3 = 0
temp_d4 = 0 
temp_d5 = 0
temp_d6 = 0 
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
	if request.method == 'POST': #form.validate_on_submit():
		print(form.dc1.data)
		cuserval.d1 = form.dc1.data
		cuserval.d2 = form.dc2.data
		cuserval.d3 = form.dc3.data
		cuserval.d4 = form.dc4.data
		cuserval.d5 = form.dc5.data
		cuserval.d6 = form.dc6.data
		print(cuserval.d1)
		print(cuserval.d2)
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
		
		userval = Userval(d1=0,d2=0,d3=0,d4=0,d5=0,d6=0)
		db.session.add(userval)
		db.session.commit()
		flash('You are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)
	

@app.route('/api/data', methods=['GET'])
def get_tasks():
	global temp_d1
	global temp_d2
	global temp_d3
	global temp_d4
	global temp_d5
	global temp_d6
	print('HELLO')
	print(request.remote_addr)
	if current_user.is_authenticated:
		#temp = current_user.id
		cuserval = Userval.query.get(current_user.id)
		temp_d1 = cuserval.d1
		temp_d2 = cuserval.d2
		temp_d3 = cuserval.d3
		temp_d4 = cuserval.d4
		temp_d5 = cuserval.d5
		temp_d6 = cuserval.d6
		return jsonify({'Duty Cycle 1': temp_d1, 'Duty Cycle 2': temp_d2, 'Duty Cycle 3': temp_d3, 'Duty Cycle 4': temp_d4, 'Duty Cycle 5': temp_d5, 'Duty Cycle 6': temp_d6})
	return jsonify({'Duty Cycle 1': temp_d1, 'Duty Cycle 2': temp_d2, 'Duty Cycle 3': temp_d3, 'Duty Cycle 4': temp_d4, 'Duty Cycle 5': temp_d5, 'Duty Cycle 6': temp_d6})
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
