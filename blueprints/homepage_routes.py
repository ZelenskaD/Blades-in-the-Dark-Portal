import os
from flask import Blueprint, render_template, redirect, url_for,g
from schemas import Session, Campaign, Character, db
from schemas.user_models import User

template_folder_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'home')

print("Template folder absolute path:", template_folder_path)

homepage_bp = Blueprint('homepage', __name__, template_folder=template_folder_path)


@homepage_bp.route('/')
def show_homepage_or_main_page():
    if g.user:
        user_count = User.query.count()
        character_count = Character.query.count()
        campaign_count = Campaign.query.count()
        session_count = Session.query.count()
        playbook_count = 7  # Assuming you have 7 playbooks

        return render_template('home/main_page.html', user_count=user_count, character_count=character_count,
                               campaign_count=campaign_count, session_count=session_count, playbook_count=playbook_count)
    else:
        user_count = User.query.count()
        character_count = Character.query.count()
        campaign_count = Campaign.query.count()
        session_count = Session.query.count()
        playbook_count = 7
        return render_template('home/homepage.html', user_count=user_count, character_count=character_count,
                               campaign_count=campaign_count, session_count=session_count, playbook_count=playbook_count)







