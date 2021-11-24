from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length

class UserCreateForm(FlaskForm):
    """Form to add a new user."""
    username = StringField("Username",  validators=[
            InputRequired(message="Username can't be blank"),
            Length(min=5, max=20, message="Must be 5-20 characters long")])
    password = PasswordField("Password", validators=[
            InputRequired(message="Password is required")])
    email = EmailField("Email Address", validators=[
            InputRequired(message="Email address can't be blank"),
            Length(max=20, message="Must be less than 50 characters long")])
    first_name = StringField("First Name", validators=[
            InputRequired(message="First Name can't be blank"),
            Length(min=2, max=30, message="Must be 2-30 characters long")])
    last_name = StringField("Last Name", validators=[
            InputRequired(message="Last Name can't be blank"),
            Length(min=2, max=30, message="Must be 2-30 characters long")])

class UserLoginForm(FlaskForm):
    """Form for user login."""
    username = StringField("Username",  validators=[
            InputRequired(message="Username can't be blank"),
            Length(min=5, max=20, message="Must be 5-20 characters long")])
    password = PasswordField("Password", validators=[
            InputRequired(message="Password is required")])

class UserEditForm(FlaskForm):
    """Form for user edit."""
    email = EmailField("Email Address", validators=[
            InputRequired(message="Email address can't be blank"),
            Length(max=20, message="Must be less than 50 characters long")])
    first_name = StringField("First Name", validators=[
            InputRequired(message="First Name can't be blank"),
            Length(min=2, max=30, message="Must be 2-30 characters long")])
    last_name = StringField("Last Name", validators=[
            InputRequired(message="Last Name can't be blank"),
            Length(min=2, max=30, message="Must be 2-30 characters long")])

class FeedbackForm(FlaskForm):
    """Form to add/edit feedback on a recipe."""
    title = StringField("Title", validators=[
            InputRequired(message="Title can't be blank"),
            Length(max=100, message="Must be less than 100 characters long")])
    content = TextAreaField("Comments", validators=[
            InputRequired(message="Comments can't be blank")])