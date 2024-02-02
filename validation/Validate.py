from wtforms import StringField, PasswordField, DateField,EmailField,IntegerField,SelectField
from wtforms.validators import DataRequired, Email, Length,NumberRange,Regexp
from flask_wtf import FlaskForm
from email_validator import validate_email, EmailNotValidError


from wtforms import StringField, DateField, EmailField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, Email, NumberRange
from flask_wtf import FlaskForm

class name(FlaskForm):
    t_name = StringField('t_name', validators=[
        DataRequired(message='Name is required'),
        Length(min=3, max=20, message='Name must be between 3 and 20 characters'),
        Regexp('^[A-Za-z]*$', message='Name must contain only letters')
    ])

    # t_dob = DateField('t_dob', format='%Y-%m-%d', validators=[
    #     DataRequired(message='DOB is required. Use YYYY-MM-DD format.')
    # ])

    # t_email = EmailField('t_email', validators=[
    #     DataRequired(message='Email is required'),
    #     Email(message='Invalid email format')
    # ])

    # t_phoneno = IntegerField('t_phoneno', validators=[
    #     DataRequired(message='Phone number is required'),
    #     NumberRange(min=1000000000, max=9999999999, message='Invalid Phone number. Must be 10 digits.')
    # ])

    # username = StringField('username', validators=[
    #     DataRequired(message='Username is required'),
    #     Length(min=4, max=20, message='Username must be between 4 and 20 characters')
    # ])



class Password(FlaskForm):
    new_password = PasswordField('new_password', validators=[DataRequired(message='Userpassword is required')])



class addCourse(FlaskForm):
    c_name = StringField('c_name', validators=[DataRequired(message='Name is required'),Length(min=3, max=20),Regexp('^[A-Za-z]*$')])
    start_date = DateField('start_date', format='%Y-%m-%d', validators=[DataRequired(message='start_date required ,Use YYYY-MM-DD.')])
    coins=IntegerField('coins', validators=[DataRequired(message='coins is required')])
    assessment_no=IntegerField('assessment_no', validators=[DataRequired(message='Total assessment no. is required')])
    

class add_assessment(FlaskForm):
     as_name = StringField('as_name', validators=[DataRequired(message='Assessment ame is required'),Length(min=3, max=20),Regexp('^[A-Za-z]*$')])
     as_date = DateField('as_date', format='%Y-%m-%d', validators=[DataRequired(message='Assessment date required ,Use YYYY-MM-DD.')])
 


def validate_tutor(data):
    form = name(data=data)
    if not form.validate():
        return False, form.errors

    # Validate email using email_validator library
    try:
        validate_email(data['t_email'])
    except EmailNotValidError as e:
        return False, f'Invalid email: {str(e)}'
    return True, None

def validate_password(data):
    form = Password(data=data)
    if not form.validate():
        return False, form.errors
    
    return True, None

    
def validate_course(data):
    form = addCourse(data=data)
    if not form.validate():
        return False,form.errors
    return True, None


def validate_assessment(data):
    form = add_assessment(data=data)
    if not form.validate():
        return False,form.errors