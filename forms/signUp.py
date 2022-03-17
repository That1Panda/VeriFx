from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, MultipleFileField, IntegerField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from services.models import User

class SignUpForm(FlaskForm):
    def validate_user_id(self, user_id_to_check):
        print('v1, user_id: ',user_id_to_check.data)
        user = User.getByUserId(user_id_to_check.data)
        if user== None:
            pass
        elif user.user_id:
            raise ValidationError('user id already exists! Please try a different username')

    name = StringField('Name:', validators=[Length(min=3, max=20), DataRequired()])
    user_id = IntegerField('user id:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[Length(min=4, max=8),DataRequired()])
    confirmPassword = PasswordField('Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    images= MultipleFileField('images: ', validators=[DataRequired()])
    
    submit = SubmitField('Create Account')