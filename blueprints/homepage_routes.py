import os
from flask import Blueprint, render_template


from schemas import Session, Campaign, Character, db
from schemas.user_models import User

template_folder_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'home')

print("Template folder absolute path:", template_folder_path)

homepage_bp = Blueprint('homepage', __name__, template_folder=template_folder_path)


# @homepage_bp.route('/')
# def show_main_page():
#     from schemas.user_models import User # Import within the function to avoid circular import issues
#     users = User.query.all()
#     return render_template('home/homepage.html', users=users)


@homepage_bp.route('/')
def show_main_page():
    user_count = User.query.count()
    character_count = Character.query.count()
    campaign_count = Campaign.query.count()
    session_count = Session.query.count()

    # Count distinct playbook names

    return render_template('home/main_page.html', user_count=user_count, character_count=character_count,
                           campaign_count=campaign_count, session_count=session_count)






