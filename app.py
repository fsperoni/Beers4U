"""Flask app for Feedback"""
from flask import Flask, render_template, redirect, session, flash, request
from models import db, connect_db, User, Feedback, Favorite
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserCreateForm, UserLoginForm, UserEditForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
from helpers import add_image
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///beers4u'
app.config['SECRET_KEY'] = 'temporary_development_key'
# Delete below before deploying
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

BASE_URL = 'https://api.punkapi.com/v2'

@app.errorhandler(404)
def handle_not_found(event):
    """Show custom page whenever a 404 error is encountered."""

    return render_template('404.html')

@app.route('/')
def show_home():
    """Show home page"""
    if "username" in session:
        return redirect('/dashboard')
    return render_template("home.html")

################################################################
# User routes

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """
        Show a form that when submitted will register/create a user.
        Process the registration form by adding a new user. 
    """
    if "username" in session:
        return redirect('/dashboard')
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
        return render_template("show_user.html", user=new_user)
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """
        Show a form that when submitted will login a user. 
        Process the login form, ensuring the user is authenticated and 
        redirecting to dashboard page if so.
    """

    if "username" in session:
        return redirect('/dashboard')
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            flash(f"Welcome Back, {user.full_name}!", "primary")
            return render_template("dashboard.html", user=user)
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/users/<int:id>')
def show_user(id):
    """Display user profile."""
    
    if "username" not in session:
        form = UserLoginForm()
        flash("Please login first!", "danger")
        return render_template('login.html', form=form)
    user = User.query.get_or_404(id)
    return render_template("show_user.html", user=user)

@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    """Remove the user from the database"""

    form = UserLoginForm()
    if "username" not in session:
        flash("Please login first!", "danger")
    else:
        user = User.query.get_or_404(id)
        if session['username'] == user.username:
            db.session.delete(user)
            db.session.commit()
            session.pop('username')
            flash("Account deleted!", "success")
        else:
            flash("You can only delete your own account.", "danger")
            return render_template("show_user.html", user=user)
    return render_template('login.html', form=form)

@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    """Edit the user in the database"""

    if "username" not in session:
        form = UserLoginForm()
        flash("Please login first!", "danger")
        return render_template('login.html', form=form)
    user = User.query.get_or_404(id)
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        if session['username'] != user.username:
            flash("You can only update your own profile.", "danger")
            return render_template("show_user.html", user=user)
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        db.session.add(user)
        db.session.commit()
        flash("Profile updated!", "success")
        return render_template("show_user.html", user=user)
    else:
        return render_template("edit_user.html", form=form, user=user)

@app.route('/logout')
def user_logout():
    """ Clear any information from the session and redirect to /login """

    session.pop('username')
    flash("Goodbye!", "info")
    return render_template('home.html')

@app.route('/dashboard')
def show_dashboard():
    """Show a dashboard page"""

    if "username" not in session:
        flash("You're not logged in! Showing limited features", "info")
        return render_template('dashboard.html')
    
    user = User.query.filter(User.username == session["username"]).first()
    return render_template('dashboard.html', user=user)

################################################################
# Search routes

@app.route('/random')
def show_random_beer():
    """Get random beer recipe from API"""

    response = requests.get(f"{BASE_URL}/beers/random")
    recipes = add_image(response.json()) 

    return render_template('recipes.html', recipes=recipes)

@app.route('/search/beers', methods=["POST"])
def show_foods():
    """Search and show beer pairings based on search criteria"""

    criteria = request.form["foodInput"].strip().replace(' ', '_')
    response = requests.get(f"{BASE_URL}/beers?food={criteria}")
    beers = add_image(response.json())
    if len(beers) == 0:
        flash("No beers found for your search criteria. Please try again.", "warning")
        return render_template('dashboard.html')
    else: 
        return render_template('pairing.html', beers=beers)

@app.route('/search/foods', methods=["POST"])
def show_beers():
    """Search and show food pairings based on search criteria"""

    criteria = request.form["beerInput"].strip().replace(' ', '_')
    response = requests.get(f"{BASE_URL}/beers?beer_name={criteria}")
    beers = add_image(response.json())
    if len(beers) == 0:
        flash("No beers found for your search criteria. Please try again.", "warning")
        return render_template('dashboard.html')
    else: 
        return render_template('pairing.html', beers=beers)

@app.route('/search/recipes', methods=["POST"])
def show_recipes():
    """Search and show recipes based on search criteria"""
    
    criteria_list = [[name, value] for name, value in request.form.items() if request.form[name] ]
    criteria = '?'
    for item in criteria_list:
        criteria += f"{item[0]}={item[1]}&"
    l = len(criteria)
    criteria = criteria[:l-1] #remove extra "&"
    response = requests.get(f"{BASE_URL}/beers{criteria}")
    recipes = add_image(response.json())
    if len(recipes) == 0:
        flash("No beers found for your search criteria. Please try again.", "warning")
        return render_template('dashboard.html')
    else: 
        return render_template('recipes.html', recipes=recipes)

    