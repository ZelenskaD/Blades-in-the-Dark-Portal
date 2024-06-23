import os
from flask import Blueprint, render_template
from flask import Flask, render_template
import requests

BLADES_URL = "https://blades-portal-api.surganov.dev"

template_folder_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'characters')

print("Template folder absolute path:", template_folder_path)

characters_bp = Blueprint('characters', __name__, template_folder=template_folder_path)


@characters_bp.route('/create')
def create_character():
    response = requests.get(f"{BLADES_URL}/playbooks")
    if response.status_code == 200:
        campaigns = response.json()
    else:
        campaigns = []
    return render_template('characters/create_character_form.html')

