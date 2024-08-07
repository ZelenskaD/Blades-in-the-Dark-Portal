
from flask import Blueprint, render_template, redirect, url_for, session, flash, g, request
from form_requests.campaign_forms import AddCampaignForm, EditCampaignForm

from schemas import db, Character
from schemas.campaign_models import Campaign
from schemas.user_models import User
from schemas.session_models import Session

campaigns_bp = Blueprint('campaigns', __name__, template_folder='templates/campaigns')


@campaigns_bp.route('/create_campaign', methods=['GET', 'POST'])
def create_campaign():
    form = AddCampaignForm()
    if form.validate_on_submit():
        user_id = session.get('curr_user')
        if not user_id:
            flash('User not authenticated', 'danger')
            return redirect(url_for('auth.login_user'))

        user = User.query.get(user_id)
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('auth.login_user'))

        campaign_picture = form.campaign_picture.data or 'backgrounds/default-card.png'
        campaign = Campaign(
            name=form.name.data,
            description=form.description.data,
            campaign_picture=campaign_picture,
            creator_id=user.id,
        )
        db.session.add(campaign)
        db.session.commit()
        flash('Campaign created!', 'success')
        return redirect(url_for('campaigns.my_campaigns'))

    return render_template('campaigns/create_campaign_form.html', form=form)


@campaigns_bp.route('/edit_campaign/<int:campaign_id>', methods=['GET', 'POST'])
def edit_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    form = EditCampaignForm(obj=campaign)

    if form.validate_on_submit():
        if 'curr_user' not in session or session['curr_user'] != campaign.creator_id:
            flash('You do not have permission to edit this campaign', 'danger')
            return redirect(url_for('homepage.show_homepage_or_main_page'))

        campaign.name = form.name.data
        campaign.description = form.description.data
        campaign.campaign_picture = form.campaign_picture.data or campaign.campaign_picture

        db.session.commit()
        flash('Campaign updated successfully!', 'success')
        return redirect(url_for('campaigns.show_campaign', campaign_id=campaign.id))

    return render_template('campaigns/edit_campaign.html', form=form, campaign=campaign)


@campaigns_bp.route('/delete/<int:campaign_id>', methods=['GET'])
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign deleted successfully!', 'success')
    return redirect(url_for('campaigns.my_campaigns'))


@campaigns_bp.route('/<int:campaign_id>')
def show_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)

    page_sessions = request.args.get('page_sessions', 1, type=int)
    page_characters = request.args.get('page_characters', 1, type=int)

    sessions_pagination = Session.query.filter_by(campaign_id=campaign_id).order_by(Session.created_at.desc()).paginate(page=page_sessions, per_page=6, error_out=False)
    characters_pagination = Character.query.filter_by(campaign_id=campaign_id).paginate(page=page_characters, per_page=6, error_out=False)

    sessions = sessions_pagination.items
    characters = characters_pagination.items

    return render_template('campaigns/show_campaign.html', campaign=campaign, sessions=sessions,
                           characters=characters, sessions_pagination=sessions_pagination,
                           characters_pagination=characters_pagination)


@campaigns_bp.route('/my_campaigns', methods=['GET'])
def my_campaigns():
    user_id = session.get('curr_user')
    if not user_id:
        flash('Please log in to view your campaigns', 'danger')
        return redirect(url_for('auth.login_user'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('auth.login_user'))

    page = request.args.get('page', 1, type=int)
    per_page = 3
    campaigns_pagination = Campaign.query.filter_by(creator_id=user.id).paginate(page, per_page, False)
    campaigns = campaigns_pagination.items

    return render_template('campaigns/my_campaigns.html', campaigns=campaigns, pagination=campaigns_pagination)


@campaigns_bp.route('/join_campaign', methods=['GET', 'POST'])
def join_campaign():
    user_id = session.get('curr_user')
    print(f"user_id from session: {user_id}")

    if not user_id:
        flash('Please log in to join campaigns', 'danger')
        return redirect(url_for('auth.login_user'))

    if request.method == 'POST':
        campaign_id = request.form.get('campaign_id')
        character_id = request.form.get('character_id')

        # Fetch the character and campaign from the database
        character = Character.query.filter_by(id=character_id, user_id=g.user.id).first()
        campaign = Campaign.query.get(campaign_id)

        if not character or not campaign:
            flash('Invalid campaign ID or character.', 'danger')
            return redirect(url_for('campaigns.join_campaign'))

        # Add the character to the campaign
        character.campaign_id = campaign.id
        db.session.commit()

        flash('Successfully joined the campaign!')
        return redirect(url_for('campaigns.show_campaign', campaign_id=campaign_id))

    # Get all characters created by the current user
    characters = Character.query.filter_by(user_id=g.user.id, campaign_id=None).all()
    campaigns = Campaign.query.all()  # Fetch all campaigns

    return render_template('campaigns/join_campaign_form.html', characters=characters, campaigns=campaigns)


@campaigns_bp.route('/leave_campaign', methods=['POST'])
def leave_campaign():
    character_id = request.form.get('character_id')
    character = Character.query.get(character_id)

    if character and character.user_id == session.get('curr_user'):
        character.campaign_id = None
        db.session.commit()
        flash('You have left the campaign.', 'success')
    else:
        flash('Invalid operation.', 'danger')

    return redirect(url_for('campaigns.participating_campaigns'))


@campaigns_bp.route('/participating_campaigns')
def participating_campaigns():
    user_id = session.get('curr_user')
    print(f"user_id from session: {user_id}")
    if not user_id:
        flash('Please log in to join campaigns', 'danger')
        return redirect(url_for('auth.login_user'))

    page = request.args.get('page', 1, type=int)
    characters_pagination = Character.query.filter_by(user_id=user_id).paginate(page=page, per_page=3, error_out=False)

    return render_template('campaigns/participating_campaigns.html', characters_pagination=characters_pagination)


@campaigns_bp.route('/remove_character', methods=['POST'])
def remove_character():
    character_id = request.form.get('character_id')
    campaign_id = request.form.get('campaign_id')
    character = Character.query.get(character_id)
    campaign = Campaign.query.get(campaign_id)

    if character and campaign and g.user.id == campaign.creator_id:
        character.campaign_id = None
        db.session.commit()
        flash('Character has been removed from the campaign.', 'success')
    else:
        flash('Invalid operation.', 'danger')

    return redirect(url_for('campaigns.show_campaign', campaign_id=campaign_id))


