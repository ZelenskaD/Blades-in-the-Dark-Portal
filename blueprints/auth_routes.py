from flask import render_template, redirect, url_for, flash, session, g, Blueprint, flash
from sqlalchemy.exc import IntegrityError

from form_requests.auth_forms import SignUpForm, LoginForm
from schemas.user_models import User

CURR_USER_KEY = "curr_user"

auth_bp = Blueprint('auth', __name__, template_folder='templates/auth')


@auth_bp.before_app_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@auth_bp.route('/signup', methods=['GET', 'POST'])
def show_sign_up_form():
    import os
    print("Current Working Directory:", os.getcwd())
    print("Expected Template Path:", os.path.join(os.getcwd(), 'templates/auth/sign_up_form.html'))

    form = SignUpForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            do_login(user)
            flash(f"Welcome, {user.username}! Your account was successfully created.", "success")
            return redirect(url_for('homepage.show_homepage_or_main_page'))

        except IntegrityError:
            flash("Username or email already taken", 'danger')
            return render_template('auth/sign_up_form.html', form=form)
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'danger')
            return render_template('auth/sign_up_form.html', form=form)

    return render_template('auth/sign_up_form.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            do_login(user)
            session['curr_user'] = user.id
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for('homepage.show_homepage_or_main_page'))  # Use endpoint name
        else:
            flash("User not found. Check your password or username.", 'danger')

    return render_template('auth/login_form.html', form=form)  # Corrected template path


@auth_bp.route('/logout')
def logout():
    """Handle logout of user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    flash('Successfully logged out!', 'success')
    return redirect(url_for('homepage.show_homepage_or_main_page'))





