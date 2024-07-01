import logging
import os


from flask import Blueprint
from flask import redirect, url_for, session, flash, jsonify, request
from flask import render_template

from clients import blades_api_client
from form_requests.character_forms import ChoosePlaybookForm, set_playbook_choices, CreateCharacterForm, \
    set_character_choices, EditSkillsForm, EditAbilitiesForm, EditExperienceForm, EditStressForm
from schemas import User, Character, db
from schemas.decorators.abilities_type import Ability

# from schemas.decorators.experience_type import Experience
from schemas.decorators.insight_type import Insight
from schemas.decorators.prowess_type import Prowess
from schemas.decorators.resolve_type import Resolve
from schemas.decorators.stress_type import Stress
from schemas.decorators.trauma_type import Trauma
from schemas.decorators.contact_type import Contact

template_folder_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'characters')

print("Template folder absolute path:", template_folder_path)

characters_bp = Blueprint('characters', __name__, template_folder=template_folder_path)


@characters_bp.route('/choose-playbook')
def choose_playbook():
    playbooks = blades_api_client.get_playbooks()
    form = ChoosePlaybookForm()
    set_playbook_choices(form, playbooks)

    if form.name.choices:
        return render_template('characters/create_playbook_form.html', form=form)
    else:
        flash('An error has occurred.', 'danger')
        return redirect(url_for('homepage.show_main_page'))


@characters_bp.route('/create-character', methods=['POST'])
def create_character():
    form = ChoosePlaybookForm()

    playbooks = blades_api_client.get_playbooks()
    set_playbook_choices(form, playbooks)

    if form.validate_on_submit():
        if 'curr_user' not in session:
            flash('You do not have permission to create a character', 'danger')
            return redirect(url_for('homepage.show_main_page'))

        playbook_name = form.name.data
        playbook = next((playbook for playbook in playbooks if playbook['name'] == playbook_name), None)

        character_form = CreateCharacterForm()
        character_form.name.data = None

        set_character_choices(character_form, playbook)

        return render_template('characters/create_character_form.html', playbook=playbook_name, form=character_form)
    else:
        flash('An error has occurred.', 'danger')
        return render_template('characters/create_playbook_form.html', form=form)


@characters_bp.route('/submit-character/<playbook_name>', methods=['POST'])
def submit_character(playbook_name):
    form = CreateCharacterForm()
    playbook = blades_api_client.get_playbook(playbook_name)
    set_character_choices(form, playbook)

    if form.enemy.data == form.friend.data:
        flash('You cannot have the same friend and enemy', 'warning')
        return render_template('characters/create_character_form.html', playbook=playbook_name, form=form)

    if form.validate_on_submit():
        user_id = session['curr_user']
        if not user_id:
            flash('User not authenticated', 'danger')
            return redirect(url_for('auth.login_user'))

        user = User.query.get(user_id)
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('auth.login_user'))

        # Ability
        api_ability = next(
            (ability for ability in playbook["specialAbilities"] if ability['name'] == form.ability.data), None)
        ability = Ability(name=api_ability['name'], description=api_ability['description'])

        # Insight ... is being directly assigned instead of its dictionary representation.

        # Insight
        insight = Insight.from_dict(playbook["attributes"]["insightDefaults"]).to_dict()

        # Prowess
        prowess = Prowess.from_dict(playbook["attributes"]["prowessDefaults"]).to_dict()

        # Resolve
        resolve = Resolve.from_dict(playbook["attributes"]["resolveDefaults"]).to_dict()
        print(f"Prowess: {prowess}")
        print(f"Resolve: {resolve}")

        # XP
        # experience = Experience(current=0, maximum=playbook["attributes"]["playbookExpPoints"]).to_dict()

        # Stress
        stress = Stress(current=0, maximum=playbook["attributes"]["stressPoints"]).to_dict()

        # Trauma
        trauma = Trauma(current=0, maximum=playbook["attributes"]["traumaPoints"]).to_dict()
        print(f"Raw Trauma Data: {trauma}")
        # print(f"Experience: {experience}")
        print(f"Stress: {stress}")
        print(f"Trauma: {trauma}")
        # Contacts
        api_friend = next((friend for friend in playbook['contacts'] if friend['name'] == form.friend.data), {})
        api_enemy = next((enemy for enemy in playbook['contacts'] if enemy['name'] == form.enemy.data), {})

        print(f"Raw Friend Data: {api_friend}")
        print(f"Raw Enemy Data: {api_enemy}")

        friend = Contact.from_dict(api_friend).to_dict()
        enemy = Contact.from_dict(api_enemy).to_dict()

        character = Character(
            name=form.name.data,
            alias=form.alias.data,
            look=form.look.data,
            heritage=form.heritage.data,
            background=form.background.data,
            vice=form.vice.data,
            user_id=user_id,
            abilities=[ability],
            insight=insight,
            prowess=prowess,
            resolve=resolve,
            experience=form.experience.data or 0,
            stress=stress,
            trauma=trauma,
            friend=friend,
            enemy=enemy,
            campaign_id=None,
            playbook_name=playbook_name
        )

        db.session.add(character)
        db.session.commit()

        flash('Character successfully created.', 'success')
        return redirect(url_for('characters.show_character', character_id=character.id))
        # return render_template('characters/show_all_characters.html', playbook=playbook, form=form)
    else:
        flash('An error has occurred.', 'danger')
        return redirect(url_for('homepage.show_main_page'))


@characters_bp.route('/my_characters', methods=['GET'])
def show_all_characters():
    user_id = session.get('curr_user')
    if not user_id:
        flash('Please log in to view your characters', 'danger')
        return redirect(url_for('auth.login_user'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('auth.login_user'))

    characters = Character.query.filter_by(user_id=user_id).all()

    return render_template('characters/show_all_characters.html', characters=characters)


@characters_bp.route('/show/<int:character_id>', methods=['GET'])
def show_character(character_id):
    print(f"Fetching character with ID: {character_id}")
    try:
        character = Character.query.get_or_404(character_id)
        print(f"Character data: {character}")
    except Exception as e:
        print(f"Error fetching character: {e}")
        return "Error fetching character", 500

    return render_template('characters/show_character.html', character=character)


@characters_bp.route('/edit-skills/<int:character_id>', methods=['GET'])
def edit_skills(character_id):
    character = Character.query.get_or_404(character_id)

    form = EditSkillsForm()

    # Populate the form with existing skills from the character
    form.hunt.data = character.insight.get('hunt', 0)
    form.study.data = character.insight.get('study', 0)
    form.survey.data = character.insight.get('survey', 0)
    form.tinker.data = character.insight.get('tinker', 0)
    form.finnesse.data = character.prowess.get('finnesse', 0)
    form.prowl.data = character.prowess.get('prowl', 0)
    form.skirmish.data = character.prowess.get('skirmish', 0)
    form.wreck.data = character.prowess.get('wreck', 0)
    form.attune.data = character.resolve.get('attune', 0)
    form.command.data = character.resolve.get('command', 0)
    form.consort.data = character.resolve.get('consort', 0)
    form.sway.data = character.resolve.get('sway', 0)

    return render_template('characters/character_skills_edit.html', form=form, character=character)


@characters_bp.route('/submit-skills/<int:character_id>', methods=['POST'])
def submit_skills(character_id):
    form = EditSkillsForm()
    character = Character.query.get_or_404(character_id)

    if form.validate_on_submit():
        # Update character's skills in the database
        character.insight = {
            'hunt': form.hunt.data,
            'study': form.study.data,
            'survey': form.survey.data,
            'tinker': form.tinker.data,
        }
        character.prowess = {
            'finnesse': form.finnesse.data,
            'prowl': form.prowl.data,
            'skirmish': form.skirmish.data,
            'wreck': form.wreck.data,
        }
        character.resolve = {
            'attune': form.attune.data,
            'command': form.command.data,
            'consort': form.consort.data,
            'sway': form.sway.data,
        }

        db.session.commit()

        flash('Skills successfully updated.', 'success')
        return redirect(url_for('characters.show_character', character_id=character.id))
    else:
        # Print validation errors for debugging
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")

        # Print form data for debugging
        print("Form data:")
        print(f"Hunt: {form.hunt.data}")
        print(f"Study: {form.study.data}")
        print(f"Survey: {form.survey.data}")
        print(f"Tinker: {form.tinker.data}")
        print(f"Finnesse: {form.finnesse.data}")
        print(f"Prowl: {form.prowl.data}")
        print(f"Skirmish: {form.skirmish.data}")
        print(f"Wreck: {form.wreck.data}")
        print(f"Attune: {form.attune.data}")
        print(f"Command: {form.command.data}")
        print(f"Consort: {form.consort.data}")
        print(f"Sway: {form.sway.data}")

        flash('An error has occurred.', 'danger')
        return render_template('characters/character_skills_edit.html', form=form, character=character)


@characters_bp.route('/edit-abilities/<int:character_id>', methods=['GET', 'POST'])
def edit_abilities(character_id):
    character = Character.query.get_or_404(character_id)
    playbook = blades_api_client.get_playbook(character.playbook_name)
    form = EditAbilitiesForm()

    # Populate the abilities choices from the playbook API response
    form.abilities.choices = [(str(i), ability['name']) for i, ability in enumerate(playbook["specialAbilities"])]

    # Create a dictionary for ability descriptions
    abilities_descriptions = {str(i): ability['description'] for i, ability in enumerate(playbook["specialAbilities"])}

    if form.validate_on_submit():
        ability_index = form.abilities.data
        selected_ability = playbook["specialAbilities"][int(ability_index)]
        db_ability = Ability(name=selected_ability['name'], description=selected_ability['description'])
        character.abilities = character.abilities + [db_ability]
        db.session.commit()
        flash('Abilities successfully updated.', 'success')
        return redirect(url_for('characters.show_character', character_id=character.id))

    return render_template('characters/character_abilities_edit.html', form=form, character=character,
                           abilities_descriptions=abilities_descriptions)







@characters_bp.route('/edit-exp/<int:character_id>', methods=['GET', 'POST'])
def edit_exp(character_id):
    character = Character.query.get_or_404(character_id)
    form = EditExperienceForm(obj=character)

    if form.validate_on_submit():
        character.experience = form.experience.data
        db.session.commit()
        flash('Experience successfully updated.', 'success')
        return redirect(url_for('characters.show_character', character_id=character.id))

    return render_template('characters/character_exp_edit.html', form=form, character=character)


@characters_bp.route('/edit-stress/<int:character_id>', methods=['GET', 'POST'])
def edit_stress(character_id):
    character = Character.query.get_or_404(character_id)
    form = EditStressForm()

    if form.validate_on_submit():
        character.stress['current'] = form.stress.data

        # Update trauma if stress reaches maximum
        if character.stress['current'] >= character.stress['maximum']:
            character.stress['current'] = character.stress['maximum']
            character.trauma['current'] += 1
            if character.trauma['current'] > 4:
                character.trauma['current'] = 4

        db.session.commit()
        flash('Stress successfully updated.', 'success')
        return redirect(url_for('characters.show_character', character_id=character.id))

    return render_template('characters/character_stress_edit.html', form=form, character=character)





