
from wtforms import StringField, PasswordField, DateField,EmailField,IntegerField,SelectField
from wtforms.validators import DataRequired, Email, Length,NumberRange,Regexp
from flask_wtf import FlaskForm
from validate_email_address import validate_email

# Now you can use the validate_email function


class tutorPassword(FlaskForm):
    new_password = PasswordField('new_password', validators=[DataRequired(message='Userpassword is required')])


class tutorUpdation(FlaskForm):
    t_name = StringField('t_name', validators=[DataRequired(message='Name is required'),Length(min=3, max=20),Regexp('^[A-Za-z]*$', message='name must contain only letters')])
    t_dob = DateField('t_dob', format='%Y-%m-%d', validators=[DataRequired(message='DOB required ,Use YYYY-MM-DD.')])
    t_email = EmailField('t_email', validators=[DataRequired(message='email is required'), Email()])
    t_phoneno = IntegerField('t_phoneno', validators=[DataRequired(message='Phone number required is required'),NumberRange(min=1000000000, max=9999999999,message='Invalid Phone number. Must be 10 digits.')])
    username = StringField('username', validators=[DataRequired(message='Username is required'),Length(min=4, max=20)])
    
class addcourse():
    c_name = StringField('c_name', validators=[DataRequired(message='Name is required'),Length(min=3, max=20),Regexp('^[A-Za-z]*$')])
    start_date = DateField('start_date', format='%Y-%m-%d', validators=[DataRequired(message='start_date required ,Use YYYY-MM-DD.')])
    coins=IntegerField('coins', validators=[DataRequired(message='coins is required')])
    assessment_no=IntegerField('assessment_no', validators=[DataRequired(message='Total assessment no. is required')])
    

class addassessment():
     as_name = StringField('as_name', validators=[DataRequired(message='Assessment ame is required'),Length(min=3, max=20),Regexp('^[A-Za-z]*$')])
     as_date = DateField('as_date', format='%Y-%m-%d', validators=[DataRequired(message='Assessment date required ,Use YYYY-MM-DD.')])
 

