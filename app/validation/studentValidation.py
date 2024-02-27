from wtforms import StringField, PasswordField, DateField,EmailField,IntegerField,SelectField
from wtforms.validators import Optional,Email, DataRequired,Length,NumberRange,Regexp
from flask_wtf import FlaskForm
from email_validator import validate_email, EmailNotValidError



class StudentUpdate(FlaskForm):
    s_name = StringField('s_name', validators=[Optional(), Length(min=3, max=20),Regexp('^[A-Za-z]*$', message='name must contain only letters')])
    s_dob = DateField('s_dob', format='%Y-%m-%d', validators=[Optional(),DataRequired(message='Use YYYY-MM-DD.')])
    s_email = EmailField('s_email', validators=[Optional(),DataRequired(message='Email is required'), Email()])
    s_phoneno = IntegerField('s_phoneno', validators=[Optional(),NumberRange(min=1000000000, max=9999999999,message='Invalid Phone number. Must be 10 digits.')])
    s_houseno = StringField('s_houseno', validators=[Optional(),DataRequired(message='House number required')])
    s_city = StringField('s_city', validators=[Optional(),Length(min=4, max=20),Regexp('^[A-Za-z]*$', message='Country must contain only letters')])
    s_state = StringField('s_state', validators=[Optional(),Length(min=3, max=20), Regexp('^[A-Za-z]*$', message='Country must contain only letters')])
    s_country = StringField('s_country', validators=[Optional(),Length(min=4, max=20),Regexp('^[A-Za-z]*$', message='Country must contain only letters')])
    s_pin = IntegerField('s_pin', validators=[Optional(),NumberRange(min=100000, max=999999,message='Invalid PIN. Must be 4 digits.')])

class scorevalidation(FlaskForm):
    score = IntegerField('score', validators=[DataRequired(message='score is required'),NumberRange(min=0, max=10,message='score between 0 to 10.')])
    #student_id = StringField('student_id', validators=[DataRequired(message='student_id required')])
    def validate(self):
        # Skip validation for fields that are not provided during the update
        if not super().validate():
            return False
    
        fields_to_skip = ['s_name', 's_dob', 's_email', 's_phoneno']
        for field in fields_to_skip:
            if not getattr(self, field).data:
                continue
            getattr(self, field).errors.clear()
                
        return True
    
def validate_update_student(data):
    form = StudentUpdate(data=data)
    if not form.validate():
        return False, form.errors
    return True,None
def validate_score(score):
    form = StudentUpdate(data=score)
    if not form.validate():
        return False, form.errors
    return True,None
