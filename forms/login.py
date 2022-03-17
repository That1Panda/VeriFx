from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import  DataRequired
from flask_wtf.file import FileField

class LoginForm(FlaskForm):
    
    user_id = StringField('ID:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    image=FileField('Image: ',validators=[DataRequired()])
    submit = SubmitField('Login')