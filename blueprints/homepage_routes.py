import os
from flask import Blueprint, render_template

from schemas.user_models import User
# from blueprints.auth_routes import  CURR_USER_KEY
# Define the absolute path to the template folder
template_folder_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'home')

print("Template folder absolute path:", template_folder_path)

homepage_bp = Blueprint('homepage', __name__, template_folder=template_folder_path)

#
# @homepage_bp.route('/')
# def home():
#     return render_template('homepage.html')


@homepage_bp.route('/')
def show_main_page():
    return render_template('homepage.html')



