from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Optional, NumberRange, URL


class ChoosePlaybookForm(FlaskForm):
    name = SelectField('Playbook Name', validators=[DataRequired()], choices=[])


def set_playbook_choices(form: ChoosePlaybookForm, playbooks: list):
    form.name.choices = [''] + [playbook['name'] for playbook in playbooks]


class CreateCharacterForm(FlaskForm):
    name = StringField('Character Name', validators=[DataRequired()])
    alias = StringField('Alias', validators=[DataRequired()])
    look = StringField('Appearance', validators=[Optional()])

    heritage = SelectField('Heritage', validators=[DataRequired()], choices=[])
    background = SelectField('Background', validators=[DataRequired()], choices=[])
    vice = SelectField('Vice', validators=[DataRequired()], choices=[])

    ability = SelectField('Starting Ability', validators=[DataRequired()], choices=[])
    experience = IntegerField('Experience', validators=[NumberRange(min=0, max=9)], default=0)

    friend = SelectField('Friend', validators=[DataRequired()], choices=[])
    enemy = SelectField('Enemy', validators=[DataRequired()], choices=[])


def set_character_choices(form: CreateCharacterForm, playbook: dict):
    # Heritage
    heritage_options = [''] + playbook['options']['heritageOptions']
    form.heritage.choices = heritage_options

    # Background
    background_options = [''] + playbook['options']['backgroundOptions']
    form.background.choices = background_options

    # Vice
    vice_options = [''] + playbook['options']['viceOptions']
    form.vice.choices = vice_options

    # Special Abilities
    special_abilities = playbook['specialAbilities']
    ability = [''] + [ability['name'] for ability in special_abilities]
    form.ability.choices = ability

    contacts = playbook['contacts']

    friend_options = [''] + [contact['name'] for contact in contacts]
    form.friend.choices = friend_options

    enemy_options = [''] + [contact['name'] for contact in contacts]
    form.enemy.choices = enemy_options


class EditSkillsForm(FlaskForm):
    hunt = IntegerField('Hunt', validators=[Optional(), NumberRange(min=0)])
    study = IntegerField('Study', validators=[Optional(), NumberRange(min=0)])
    survey = IntegerField('Survey', validators=[Optional(), NumberRange(min=0)])
    tinker = IntegerField('Tinker', validators=[Optional(), NumberRange(min=0)])
    finnesse = IntegerField('Finnesse', validators=[Optional(), NumberRange(min=0)])
    prowl = IntegerField('Prowl', validators=[Optional(), NumberRange(min=0)])
    skirmish = IntegerField('Skirmish', validators=[Optional(), NumberRange(min=0)])
    wreck = IntegerField('Wreck', validators=[Optional(), NumberRange(min=0)])
    attune = IntegerField('Attune', validators=[Optional(), NumberRange(min=0)])
    command = IntegerField('Command', validators=[Optional(), NumberRange(min=0)])
    consort = IntegerField('Consort', validators=[Optional(), NumberRange(min=0)])
    sway = IntegerField('Sway', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Save Skills')


class EditAbilitiesForm(FlaskForm):
    abilities = SelectField('Abilities', choices=[], coerce=str, validators=[DataRequired()])
    submit = SubmitField('Save Abilities')


class EditExperienceForm(FlaskForm):
    experience = IntegerField('Experience', validators=[DataRequired(), NumberRange(min=0, max=9)])
    submit = SubmitField('Save Experience')


class EditStressForm(FlaskForm):
    stress = IntegerField('Stress', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Save Stress')

