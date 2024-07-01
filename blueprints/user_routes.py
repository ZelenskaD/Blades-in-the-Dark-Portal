

from flask import Blueprint, render_template, redirect, url_for, session, flash, g, request

from blueprints.auth_routes import do_logout
from form_requests.user_forms import EditUserForm
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


@users_bp.route('/delete_profile', methods=["POST"])
def delete_profile():
    """Delete user."""

    if 'curr_user' not in session:
        flash("Access unauthorized.", "danger")
        return redirect(url_for('homepage.show_main_page'))

    user = User.query.get(session['curr_user'])
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('homepage.show_main_page'))

    do_logout()

    db.session.delete(user)
    db.session.commit()

    flash("Profile deleted successfully!", "success")
    return redirect(url_for('homepage.show_main_page'))


@users_bp.route('/edit_profile', methods=["GET", "POST"])
def edit_profile():
    """Edit profile for current user."""
    if 'curr_user' not in session:
        flash('Please log in to access your profile', 'danger')
        return redirect(url_for('auth.login_user'))

    user = User.query.get(session['curr_user'])
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('homepage.show_main_page'))

    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        # Validate the current password if a new password is provided
        if form.new_password.data:
            if not form.current_password.data or not bcrypt.check_password_hash(user.password_hash, form.current_password.data):
                flash("Invalid current password", "danger")
                return redirect(url_for('users.edit_profile'))

            # If current password is correct, update the user's password
            user.password_hash = bcrypt.generate_password_hash(form.new_password.data).decode('UTF-8')

        # Update the user's information
        user.username = form.username.data
        user.email = form.email.data

        db.session.commit()
        flash("Profile updated successfully!", 'success')
        return redirect(url_for('homepage.show_main_page'))

    return render_template('users/edit_profile_form.html', form=form, user=user)
