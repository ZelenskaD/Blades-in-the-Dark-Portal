from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password_current = PasswordField('Current Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[
        Length(min=6),
        EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('Confirm New Password')




