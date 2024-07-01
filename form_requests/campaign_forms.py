from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class AddCampaignForm(FlaskForm):
    name = StringField('Campaign Name', validators=[DataRequired(), Length(min=2, max=128)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1000)])
    campaign_picture = StringField('(Optional) Campaign Picture', validators=[Optional(), Length(max=1000)],
                                   default='/backgrounds/default-card.png')


class EditCampaignForm(FlaskForm):
    name = StringField('Campaign Name', validators=[DataRequired(), Length(min=2, max=128)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1000)])
    campaign_picture = StringField('(Optional) Campaign Picture', validators=[Optional()],
                                   default='/backgrounds/campaign_back.jpg')


