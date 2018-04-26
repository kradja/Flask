from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import IntegerRangeField
from app.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField(
		'Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')
	
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')
	
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
	
class InputForm(FlaskForm):
	dc1 = IntegerRangeField('Duty Cycle 1', validators=[DataRequired()])
	dc2 = IntegerRangeField('Duty Cycle 2', validators=[DataRequired()])
	dc3 = IntegerRangeField('Duty Cycle 3', validators=[DataRequired()])
	dc4 = IntegerRangeField('Duty Cycle 4', validators=[DataRequired()])
	dc5 = IntegerRangeField('Duty Cycle 5', validators=[DataRequired()])
	dc6 = IntegerRangeField('Duty Cycle 6', validators=[DataRequired()])
	
	cv = BooleanField('Current or Voltage', validators=[DataRequired()])
	submit = SubmitField('Send')