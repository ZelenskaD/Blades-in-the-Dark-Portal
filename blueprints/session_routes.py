import os
from datetime import datetime
from urllib import request

from schemas import db
from flask import Blueprint, render_template, flash, url_for, redirect, request, g, jsonify, session
from form_requests.session_forms import AddNewSession, EditSessionForm
from schemas.session_models import Session
from schemas.campaign_models import Campaign

template_folder_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'sessions')

print("Template folder absolute path:", template_folder_path)

sessions_bp = Blueprint('session', __name__, template_folder=template_folder_path)


@sessions_bp.route('/<int:campaign_id>/new_session', methods=['GET', 'POST'])
def add_session(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    form = AddNewSession()

    if g.user is None or g.user.id != campaign.creator_id:
        flash('You do not have permission to add a session to this campaign', 'danger')
        return redirect(url_for('homepage.show_homepage_or_main_page'))

    if form.validate_on_submit():
        current_time = datetime.utcnow()
        new_session = Session(
            title=form.title.data,
            notes=form.notes.data,
            created_at=current_time,
            updated_at=current_time,
            campaign_id=campaign_id
        )
        db.session.add(new_session)
        db.session.commit()
        flash('New session has been created!', 'success')
        return redirect(url_for('campaigns.show_campaign', campaign_id=campaign_id))

    current_time = datetime.utcnow().strftime('%b %d %H:%M')
    return render_template('sessions/new_session.html', form=form, campaign=campaign, current_time=current_time)


@sessions_bp.route('/<int:session_id>/edit_session', methods=['GET', 'POST'])
def edit_session(session_id):
    session_obj = Session.query.get_or_404(session_id)
    campaign = Campaign.query.get_or_404(session_obj.campaign_id)
    form = EditSessionForm(obj=session_obj)

    if g.user is None or g.user.id != campaign.creator_id:
        flash('You do not have permission to edit this session', 'danger')
        return redirect(url_for('homepage.show_homepage_or_main_page'))

    if form.validate_on_submit():
        session_obj.title = form.title.data
        session_obj.notes = form.notes.data
        session_obj.updated_at = datetime.utcnow()

        db.session.commit()
        flash('Session has been updated successfully!', 'success')
        return redirect(url_for('campaigns.show_campaign', campaign_id=session_obj.campaign_id))

    current_time = datetime.utcnow().strftime('%b %d %H:%M')
    return render_template('sessions/edit_session.html', form=form, session=session_obj, current_time=current_time)


@sessions_bp.route('/delete/<int:session_id>', methods=['POST'])
def delete_session(session_id):
    session_obj = Session.query.get_or_404(session_id)
    campaign = Campaign.query.get_or_404(session_obj.campaign_id)

    if g.user is None or g.user.id != campaign.creator_id:
        flash('You do not have permission to delete this session', 'danger')
        return redirect(request.referrer or url_for('homepage.show_homepage_or_main_page'))

    db.session.delete(session_obj)
    db.session.commit()
    flash('Session deleted successfully!', 'success')
    return redirect(request.referrer or url_for('homepage.show_homepage_or_main_page'))



