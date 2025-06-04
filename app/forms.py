from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=30)])
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=20)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Register")


#login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

#News Form
class NewsForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content")
    author = StringField("Author")
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")
    url = StringField("URL")
    image = FileField("Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])


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