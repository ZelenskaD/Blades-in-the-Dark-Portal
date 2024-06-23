import os
from flask import Blueprint, render_template
from schemas.user_models import User

template_folder_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'home')

print("Template folder absolute path:", template_folder_path)

homepage_bp = Blueprint('homepage', __name__, template_folder=template_folder_path)


@homepage_bp.route('/')
def show_main_page():
    from schemas.user_models import User # Import within the function to avoid circular import issues
    users = User.query.all()
    return render_template('home/homepage.html', users=users)



