"""Flask app for Feedback"""
from flask import Flask, render_template, redirect, session, flash, request, g
from models import db, connect_db, User, Feedback, Favorite
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserCreateForm, UserLoginForm, UserEditForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
from helpers import add_image, get_id_query_string, get_recipe_query_string
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
CURR_USER = 'current_user'

@app.before_request
def add_user_to_g():
    """If logged in, add curr user to Flask global."""

    if CURR_USER in session:
        g.user = User.query.get(session[CURR_USER])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER in session:
        del session[CURR_USER] 


@app.errorhandler(404)
def handle_not_found(event):
    """Show custom page whenever a 404 error is encountered."""

    return render_template('404.html')

@app.route('/')
def show_home():
    """Show home page"""
    if g.user:
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
    if g.user:
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
        do_login(new_user)
        flash('Welcome! Successfully Created Your Account!', "success")
        return render_template("show_user.html")
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """
        Show a form that when submitted will login a user. 
        Process the login form, ensuring the user is authenticated and 
        redirecting to dashboard page if so.
    """

    if g.user:
        return redirect('/dashboard')
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            do_login(user)
            flash(f"Welcome back {user.full_name}!", "primary")
            return render_template("dashboard.html")
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/users/show', methods=["POST"])
def show_user():
    """Display user profile."""
    
    if not g.user:
        form = UserLoginForm()
        flash("Please login first!", "danger")
        return render_template('login.html', form=form)
    fav_rec_ids = User.get_fav_rec_ids(g.user.id)
    fav_string = get_id_query_string(fav_rec_ids)
    if (len(fav_string) > 0):
        response = requests.get(f"{BASE_URL}/beers{fav_string}")
        favorites = add_image(response.json())
        return render_template('show_user.html', favorites=favorites, rec_ids=fav_rec_ids, fdbck_btn=True)
    return render_template('show_user.html')

@app.route('/users/delete', methods=['POST'])
def delete_user():
    """Remove the user from the database"""

    form = UserLoginForm()
    if not g.user:
        flash("Please login first!", "danger")
    else:
        do_logout()
        db.session.delete(g.user)
        db.session.commit()
        flash("Account deleted!", "success")
    return render_template('login.html', form=form)

@app.route('/users/edit', methods=['GET', 'POST'])
def edit_user():
    """Edit the user in the database"""

    if not g.user:
        form = UserLoginForm()
        flash("Please login first!", "danger")
        return render_template('login.html', form=form)
    form = UserEditForm(obj=g.user)
    if form.validate_on_submit():
        g.user.email = form.email.data
        g.user.first_name = form.first_name.data
        g.user.last_name = form.last_name.data
        db.session.commit()
        flash("Profile updated!", "success")
        fav_rec_ids = User.get_fav_rec_ids(g.user.id)
        fav_string = get_id_query_string(fav_rec_ids)
        if (len(fav_string) > 0):
            response = requests.get(f"{BASE_URL}/beers{fav_string}")
            favorites = add_image(response.json())
            return render_template('show_user.html', favorites=favorites, rec_ids=fav_rec_ids, fdbck_btn=True)
        return render_template('show_user.html')
    else:
        return render_template("edit_user.html", form=form)

@app.route('/logout')
def user_logout():
    """ Clear any information from the session and redirect to /login """

    do_logout()
    flash("Goodbye!", "info")
    return render_template('home.html')

@app.route('/dashboard')
def show_dashboard():
    """Show a dashboard page"""

    if not g.user:
        flash("You're not logged in! Showing limited features", "info")
    
    return render_template('dashboard.html')

################################################################
# Search routes

@app.route('/random')
def show_random_beer():
    """Get random beer recipe from API"""

    response = requests.get(f"{BASE_URL}/beers/random")
    recipes = add_image(response.json()) 

    return render_template('recipes.html', recipes=recipes, fdbck_btn=True)

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
        rec_ids = User.get_fav_rec_ids(g.user.id)
        if (len(rec_ids) > 0):
            return render_template('pairing.html', beers=beers, rec_ids=rec_ids)
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
        rec_ids = User.get_fav_rec_ids(g.user.id)
        if (len(rec_ids) > 0):
            return render_template('pairing.html', beers=beers, rec_ids=rec_ids)
        return render_template('pairing.html', beers=beers)


@app.route('/search/recipes', methods=["POST"])
def show_recipes():
    """Search and show recipes based on search criteria"""
    
    criteria_list = [[name, value] for name, value in request.form.items() if request.form[name]]
    criteria = get_recipe_query_string(criteria_list)
    response = requests.get(f"{BASE_URL}/beers{criteria}")
    recipes = add_image(response.json())
    if len(recipes) == 0:
        flash("No beers found for your search criteria. Please try again.", "warning")
        return render_template('dashboard.html')
    else: 
        rec_ids = User.get_fav_rec_ids(g.user.id)
        if (len(rec_ids) > 0):
            return render_template('recipes.html', recipes=recipes, rec_ids=rec_ids, fdbck_btn=True)
        return render_template('recipes.html', recipes=recipes, fdbck_btn=True)


################################################################
# Favorite routes

@app.route('/users/favorites/<int:rec_id>', methods=['POST'])
def toggle_favorite(rec_id):
    """Toggle favoriting a recipe."""

    if not g.user:
        form = UserLoginForm()
        flash("Please login first!", "danger")
        return render_template('login.html', form=form)
    fav = Favorite.query.filter(Favorite.user_id == g.user.id, Favorite.recipe_id == rec_id).first()
    if fav:
        db.session.delete(fav)
        flash("Recipe deleted from your favorites", "info")
    else: 
        flash("Recipe added to your favorites", "success")
        new_fav = Favorite(user_id=g.user.id, recipe_id=rec_id)
        db.session.add(new_fav)
    db.session.commit()
    
    rec_ids = User.get_fav_rec_ids(g.user.id)
    fav_string = get_id_query_string(rec_ids)
    if (len(fav_string) > 0):
        response = requests.get(f"{BASE_URL}/beers{fav_string}")
        favorites = add_image(response.json())
        return render_template('show_user.html', favorites=favorites, rec_ids=rec_ids, fdbck_btn=True)
    return render_template('show_user.html')


################################################################
# Feedback routes

@app.route('/recipes/<int:rec_id>', methods=['GET','POST'])
def show_recipes_comments(rec_id):
    """Show feedback made on recipes."""

    if not g.user:
        form = UserLoginForm()
        flash("Please login first!", "danger")
        return render_template('login.html', form=form)
    
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        recipe_id = rec_id
        user_id = g.user.id
        new_feedback= Feedback(title=title, content=content, recipe_id=recipe_id, 
            user_id=user_id)

        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback processed successfully!', "success")
    response = requests.get(f"{BASE_URL}/beers?ids={rec_id}")
    recipe = add_image(response.json())
    feedbacks = Feedback.query.filter(Feedback.recipe_id == rec_id).order_by(Feedback.created_at.desc()).all()
    rec_ids = User.get_fav_rec_ids(g.user.id)
    if recipe and feedbacks:
        return render_template('feedback.html', form=form, rec_ids=rec_ids,
            feedbacks=feedbacks, recipe=recipe[0], fdbck_btn=False)
    elif recipe:
        flash(f"No feedback found for {recipe[0].get('name')}", "info")
        return render_template('feedback.html', form=form, rec_ids=rec_ids, 
            recipe=recipe[0], fdbck_btn=False)
    else: 
        flash("Beer recipe not found.")
        return render_template('dashbarod.html')

@app.route('/users/feedbacks/<int:fdbck_id>/edit', methods=['GET','POST'])
def edit_feedback(fdbck_id):
    """
        Display a form to edit the user feedback.
        Processes the form and edits the feedback.
    """

    return redirect('/')

@app.route('/users/feedbacks/<int:fdbck_id>/delete', methods=['POST'])
def delete_feedback(fdbck_id):
    """Delete user feedback."""

    return redirect('/')