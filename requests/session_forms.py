from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired,  Length


class AddNewSession(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=128)])
    notes = TextAreaField('Notes', validators=[DataRequired(), Length(max=200000)])


class EditSessionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=128)])
    notes = TextAreaField('Notes', validators=[DataRequired(), Length(max=200000)])


