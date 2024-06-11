from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class EditUserForm(FlaskForm):
    """Form for editing user."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL', default='static/default_profile.png')
    header_image_url = StringField('(Optional) Header image URL', default='static/back.jpeg')
    password = PasswordField('Password', validators=[Length(min=6)])


