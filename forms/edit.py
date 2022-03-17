from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from services.models import User

class EditForm(FlaskForm):
    def validate_user_id(self, user_id_to_check):
        print('v1, user_id: ',user_id_to_check.data)
        user = User.getByUserId(user_id_to_check.data)
        if user== None:
            pass
        elif user.user_id:
            raise ValidationError('user id already exists! Please try a different username')

    name = StringField('Name:', validators=[Length(min=2, max=30), DataRequired()])
    user_id = IntegerField('user id:', validators=[ DataRequired()])
    password = PasswordField('Password:', validators=[Length(min=4, max=8), DataRequired()])
    confirmPassword = PasswordField('Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    
    submit = SubmitField('Confirm edit')