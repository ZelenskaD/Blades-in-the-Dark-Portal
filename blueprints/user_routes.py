

from flask import Blueprint, render_template, redirect, url_for, session, flash, g

from requests.user_forms import EditUserForm
from schemas import bcrypt, db
from schemas.user_models import User

users_bp = Blueprint('users', __name__, template_folder='templates/users')


@users_bp.before_app_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if 'curr_user' in session:
        g.user = User.query.get(session['curr_user'])
    else:
        g.user = None


@users_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'curr_user' not in session:
        flash('Please log in to access your profile', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['curr_user'])
    form = EditUserForm(obj=g.user)

    if form.validate_on_submit():
        # Verify the password
        if not bcrypt.check_password_hash(g.user.password, form.password.data):
            flash('Invalid password', 'danger')
            return redirect(url_for('homepage'))

            # Update user information
        g.user.username = form.username.data
        g.user.email = form.email.data
        g.user.image_url = form.image_url.data
        g.user.header_image_url = form.header_image_url.data

        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile', user_id=user.id))

    return render_template('users/show_user_profile.html', form=form, user=g.user)