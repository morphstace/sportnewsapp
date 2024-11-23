from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms.widgets import TextArea

#login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

#News Form
class NewsForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author")
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    submit =  SubmitField("Submit")
    password_hash = PasswordField('Password', validators=[DataRequired(),
         EqualTo('password_hash_confirm', message='Passwords must match.')])
    password_hash_confirm = PasswordField('Confirm password', validators=[DataRequired()])

#Create a psw form Class
class PasswordForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    submit =  SubmitField("Submit")

#Search form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")