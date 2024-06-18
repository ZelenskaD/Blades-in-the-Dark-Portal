
from flask import Blueprint, render_template, redirect, url_for, session, flash, g, request
from requests.campaign_forms import AddCampaignForm, EditCampaignForm

from schemas import db
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

        campaign_picture = form.campaign_picture.data or '/backgrounds/default-card.png'
        campaign = Campaign(
            name=form.name.data,
            description=form.description.data,
            campaign_picture=campaign_picture,  # Ensure you link the campaign to the current user
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
            return redirect(url_for('homepage.show_main_page'))

        campaign.name = form.name.data
        campaign.description = form.description.data
        campaign.campaign_picture = form.campaign_picture.data or campaign.campaign_picture

        db.session.commit()
        flash('Campaign updated successfully!', 'success')
        return redirect(url_for('campaigns.my_campaigns'))

    return render_template('campaigns/edit_campaign.html', form=form, campaign=campaign)


@campaigns_bp.route('/campaigns/delete/<int:campaign_id>', methods=['GET'])
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign deleted successfully!', 'success')
    return redirect(url_for('campaigns.my_campaigns'))


@campaigns_bp.route('/campaigns/<int:campaign_id>')
def show_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    sessions = Session.query.filter_by(campaign_id=campaign_id).order_by(Session.created_at.desc()).all()
    # return render_template('view_campaign.html', campaign=campaign, sessions=sessions)
    return render_template('campaigns/show_campaign.html', campaign=campaign, sessions=sessions,
                           )


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

    campaigns = Campaign.query.filter_by(creator_id=user.id).all()
    return render_template('campaigns/my_campaigns.html', campaigns=campaigns)


@campaigns_bp.route('/campaigns/leave/<int:campaign_id>', methods=['POST'])
def leave_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    # Logic for leaving the campaign, e.g., removing the user from the campaign
    flash('You have left the campaign.', 'success')
    return redirect(url_for('campaigns.my_campaigns'))
