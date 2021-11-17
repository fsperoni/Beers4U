"""Flask app for Feedback"""
from flask import Flask, render_template, redirect, session, flash
from models import db, connect_db, User, Feedback, Favorite
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserCreateForm, UserLoginForm, UserEditForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///beers4u'
app.config['SECRET_KEY'] = 'temporary_development_key'
# Delete below before deploying
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.errorhandler(404)
def handle_not_found(event):
    """Show custom page whenever a 404 error is encountered."""

    return render_template('404.html')

@app.route('/')
def show_home():
    """Show login or user page"""
    if "username" not in session:
        return redirect('/login')
    return redirect(f"/users/{session['username']}")

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """
        Show a form that when submitted will register/create a user.
        Process the registration form by adding a new user. 
    """

    form = UserCreateForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username already in use. Try again.')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f'/users/{username}')
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """
        Show a form that when submitted will login a user. This form should accept a username and a password.
        Process the login form, ensuring the user is authenticated and going to /secret if so.
    """
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/users/<username>')
def show_user(username):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    user = User.query.get_or_404(username)
    flash(f"Welcome Back, {user.full_name}!", "primary")
    return render_template("show_user.html", user=user)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Remove the user from the database"""

    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    user = User.query.get_or_404(username)
    if session['username'] == user.username:
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash("Account deleted!", "success")
    else:
        flash("You can only delete your own account.", "danger")
    return redirect('/login')

@app.route('/users/<username>/edit', methods=['GET', 'POST'])
def edit_user(username):
    """Edit the user in the database"""

    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    user = User.query.get_or_404(username)
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        if session['username'] != user.username:
            flash("You can only update your own profile.", "danger")
            return redirect(f'/users/{user.username}')
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        db.session.add(user)
        db.session.commit()
        flash("Profile updated!", "success")
        return redirect(f'/users/{user.username}')
    else:
        return render_template("edit_user.html", form=form)

@app.route('/logout')
def user_logout():
    """ Clear any information from the session and redirect to / """

    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/login')