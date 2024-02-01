
from wtforms import StringField, PasswordField, DateField,EmailField,IntegerField,SelectField
from wtforms.validators import DataRequired, Email, Length,NumberRange,Regexp
from flask_wtf import FlaskForm
from email_validator import validate_email, EmailNotValidError




class SignupForm(FlaskForm):
    s_name = StringField('s_name', validators=[DataRequired(message='Name is required'),Length(min=3, max=20),Regexp('^[A-Za-z]*$', message='name must contain only letters')])
    s_dob = DateField('s_dob', format='%Y-%m-%d', validators=[DataRequired(message='DOB required ,Use YYYY-MM-DD.')])
    s_email = EmailField('s_email', validators=[DataRequired(message='email is required'), Email()])
    s_phoneno = IntegerField('s_phoneno', validators=[DataRequired(message='Phone number required is required'),NumberRange(min=1000000000, max=9999999999,message='Invalid Phone number. Must be 10 digits.')])
    s_houseno = StringField('s_houseno', validators=[DataRequired(message='House number is required')])
    s_city = StringField('s_city', validators=[DataRequired(message='city is required'),Length(min=4, max=20),Regexp('^[A-Za-z]*$', message='Country must contain only letters')])
    s_state = StringField('s_state', validators=[DataRequired(message='State is required'),Length(min=3, max=20), Regexp('^[A-Za-z]*$', message='Country must contain only letters')])
    s_country = StringField('s_country', validators=[DataRequired(message='Country required'),Length(min=4, max=20),Regexp('^[A-Za-z]*$', message='Country must contain only letters')])
    s_pin = IntegerField('s_pin', validators=[DataRequired(message='Pin is required'),NumberRange(min=100000, max=999999,message='Invalid PIN. Must be 4 digits.')])
    username = StringField('username', validators=[DataRequired(message='Username is required'),Length(min=4, max=20)])
    userpassword = PasswordField('password', validators=[DataRequired(message='Userpassword is required')])
    type = SelectField('type', choices=[('admin', 'Admin'), ('student', 'Student'),('tutor','Tutor')], validators=[DataRequired(message='Type is required')])

    
class Login(FlaskForm):
    username = StringField('username', validators=[DataRequired(message='Username is required'),Length(min=4, max=20)])
    userpassword = PasswordField('password', validators=[DataRequired(message='Userpassword is required')])

class reward_validation(FlaskForm):
     reward_name= StringField('reward_name', validators=[DataRequired(message='Username is required'),Length(min=4, max=20)])

class redeemitem_validation(FlaskForm):
    item_name=StringField('reward_name', validators=[DataRequired(message='item name is required'),Length(min=4, max=20)])
    cost=IntegerField('cost', validators=[DataRequired(message='cost is required')])
    quantity=IntegerField('quantity', validators=[DataRequired(message='quantity is required')])

def validate_signup_data(data):
    form = SignupForm(data=data)
    if not form.validate():
        return False, form.errors

    # Validate email using email_validator library
    try:
        validate_email(data['s_email'])
    except EmailNotValidError as e:
        return False, f'Invalid email: {str(e)}'
    return True, None
def username_password(data):
    form=Login(data=data)
    if not form.validate():
        return False,form.errors

def check_rewardname(data):
    form = reward_validation(data=data)
    if not form.validate():
        return True ,None