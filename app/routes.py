import datetime
from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from app.forms import RegistrationForm, InputForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User, Userval


temp_d1 = 0
temp_d2 = 0 
temp_d3 = 0
temp_d4 = 0 
temp_d5 = 0
temp_d6 = 0 
temp_on_off = 0
freqlist = []
#app = Flask(__name__)
#app.config['SECRET_KEY'] = 'kradja'
@app.route("/", methods=('GET', 'POST'))
@app.route("/index", methods=('GET', 'POST'))
@login_required
def index():
	print('hello')
	global freqlist
	#form = InputForm(request.form)
	
	#if request.method == 'POST': # Validator to verify that the input fulfills some criteron.
	#	freq=request.form['frequency']
	#	print(freq)
	
	form = InputForm()

	cuserval = Userval.query.get(current_user.id)

	if request.method == 'POST': #form.validate_on_submit():
		freqlist = []

		cuserval.d1 = form.dc1.data
		cuserval.d2 = form.dc2.data
		cuserval.d3 = form.dc3.data
		cuserval.d4 = form.dc4.data
		cuserval.d5 = form.dc5.data
		cuserval.d6 = form.dc6.data
		cuserval.on_off = form.cv.data
		
		freqlist.append(steptofreq(form.dc1.data))
		freqlist.append(steptofreq(form.dc2.data))
		freqlist.append(steptofreq(form.dc3.data))
		freqlist.append(steptofreq(form.dc4.data))
		freqlist.append(steptofreq(form.dc5.data))
		freqlist.append(steptofreq(form.dc6.data))

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
	
	
	return render_template('index.html', title = 'Home', ulist = listofuses, cuserval = cuserval,form = form, freqlist = freqlist)

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
		#NEW LIST
		users = User.query.all()
		print(users)
		users.remove(User.query.get(current_user.id))
		for u in users:
			print(u)
			cuserval = Userval.query.get(u.id)
			print(cuserval.d2)
			cuserval.d1 = -1 * u.id
			cuserval.d2 = -1 * u.id
			cuserval.d3 = -1 * u.id
			cuserval.d4 = -1 * u.id
			cuserval.d5 = -1 * u.id
			cuserval.d6 = -1 * u.id
			cuserval.on_off = -1 * u.id
			print(cuserval.d2)
		db.session.commit()
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
		print(user)
		print(user.id)
		
		userval = Userval(d1=user.id,d2=user.id,d3=user.id,d4=user.id,d5=user.id,d6=user.id)
		db.session.add(userval)
		db.session.commit()
		flash('You are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)
	
def steptofreq(x):
	p1 = -0.001135023513954
	p2 = 1.286883232524425
	p3 = -5.826589364996270e+02
	p4 = 1.316885615266447e+05
	p5 = -1.485758972139023e+07
	p6 = 6.694456192160354e+08
	
	if x == None:
		x = 0
	
	res = (p1* x**5 + p2 * x**4 + p3 * x**3 + p4 * x**2 + p5 * x+ p6) * 1E-6
	return 1/res
	
@app.route('/api/data', methods=['GET'])
def get_tasks():
	global temp_d1
	global temp_d2
	global temp_d3
	global temp_d4
	global temp_d5
	global temp_d6
	global temp_on_off
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
		temp_on_off = cuserval.on_off
		
		
		return jsonify({'Duty Cycle 1': temp_d1, 'Duty Cycle 2': temp_d2, 'Duty Cycle 3': temp_d3, 'Duty Cycle 4': temp_d4, 'Duty Cycle 5': temp_d5, 'Duty Cycle 6': temp_d6, 'Current or Voltage': temp_on_off})
	return jsonify({'Duty Cycle 1': temp_d1, 'Duty Cycle 2': temp_d2, 'Duty Cycle 3': temp_d3, 'Duty Cycle 4': temp_d4, 'Duty Cycle 5': temp_d5, 'Duty Cycle 6': temp_d6, 'Current or Voltage': temp_on_off})

	
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
	
#if __name__ == "__main__":
#	app.run(host='0.0.0.0',port = 8090)
# Keeping the initialization inside routes.py makes this work
