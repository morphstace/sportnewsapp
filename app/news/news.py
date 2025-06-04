from app.news import bp
from flask import render_template, redirect, url_for, flash, request
from app.models import User, New
from app.forms import NewsForm, UserForm, PasswordForm, SearchForm
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash
from app.extensions import db
from datetime import date
import google.genai as genai
import os, requests
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename
import uuid

client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

def text_sumarization(text):
    """Function to summarize text using Google Generative AI."""
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=f"Fornisci un riassunto conciso del seguente testo:\n\n{text}"
        +"La sintesi deve essere scritta senza tradurre il testo originale e deve avere tra 500 e 1000 caratteri."
    )
    return response.text.strip() if response else "Nessun riassunto disponibile."

def text_validation(text):
    """Function to validate text grammar using Google Generative AI."""
    """Corregge gli errori grammaticali nel testo utilizzando Gemini."""
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=f"Correggi eventuali errori grammaticali nel seguente testo e restituisci il testo corretto:\n\n{text}."+
        "Rispondi solo con il testo corretto, senza spiegazioni.")
    return response.text if response else "Nessun testo corretto disponibile."

def text_retrieval(url):
    """Function to retrieve text from a URL"""
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([para.get_text() for para in paragraphs])
        print(text)
        return text.strip()
    print("Error retrieving text from URL:", res.status_code)
    return "Nessun testo recuperato dalla URL."

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/news/<int:id>')
def new(id):
    new = New.query.get_or_404(id)
    return render_template('new.html', new=new)

@bp.route('/news/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_new(id):
    new = New.query.get_or_404(id)
    form = NewsForm()
    title = new.title
    slug = new.slug
    content = new.content
    if form.validate_on_submit():
        action = request.form.get('action')
        if action == 'sintetize':
            summarized_text = text_sumarization(form.content.data)
            content = summarized_text
            title = form.title.data
            slug = form.slug.data
        elif action == 'correct':
            validated_text = text_validation(form.content.data)
            content = validated_text
            title = form.title.data
            slug = form.slug.data
        elif action == None:
            new.title = form.title.data
            new.slug = form.slug.data
            new.content = form.content.data
            db.session.add(new)
            db.session.commit()
            flash("Update successful!")
            return redirect(url_for('news.new', id=new.id))
        else:
            flash("Invalid action. Please try again.")
    if current_user.id == new.poster_id:
        form.title.data = title
        form.slug.data = slug
        form.content.data = content
        return render_template('edit_new.html', form=form)
    flash("You are not authorized to edit.")
    return render_template('new.html', new=new)
    

@bp.route('/add-news', methods=['GET','POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        action = request.form.get('action')
        if action == 'sintetize':
            summarized_text = text_sumarization(form.content.data)
            form.content.data = summarized_text
        elif action == 'correct':
            validated_text = text_validation(form.content.data)
            form.content.data = validated_text
        elif action == 'retrieve':
            retrieved_text = text_retrieval(form.url.data)
            form.content.data = retrieved_text
        elif action == None:
            image_file = form.image.data
            image_filename = None
            if image_file:
                filename = secure_filename(image_file.filename)
                unique_name = f"{uuid.uuid4().hex}_{filename}"
                image_path = os.path.join('uploads', unique_name)
                os.makedirs(os.path.dirname(os.path.join('app', 'static', image_path)), exist_ok=True)
                image_file.save(os.path.join('app','static', image_path))
                image_filename = image_path
            news = New(title=form.title.data, content=form.content.data,
            poster_id=current_user.id, slug=form.slug.data, image=image_filename, poster=current_user)
            form.title.data = ''
            form.content.data = ''
            form.slug.data = ''
            form.image.data = None
            db.session.add(news)
            db.session.commit()
            flash("News submitted successfully!")
        else:
            flash("Invalid action. Please try again.")
            return render_template("add_news.html", form=form)
    return render_template("add_news.html", form=form)

@bp.route('/news/delete/<int:id>')
@login_required
def delete_new(id):
    new_to_del = New.query.get_or_404(id)
    user_id = current_user.id
    poster_id = new_to_del.poster.id
    #if 1==1:
    if user_id == poster_id:
        try:
            db.session.delete(new_to_del)
            db.session.commit()
            flash("News deleted successfully!")
            return redirect(url_for('news.news'))
        except:
            flash("Something went wrong, try again.")
            return render_template('new.html', new=new_to_del)
    flash("You are not authorized.")
    return render_template('new.html', new=new_to_del)



@bp.route('/news')
def news():
    #grab all news from db
    news = New.query.order_by(New.date_posted)
    return render_template("news.html", news=news)

@bp.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    news = New.query
    if form.validate_on_submit():
        new.searched = form.searched.data
        news = news.filter(New.content.like('%'+new.searched+'%'))
        news = news.order_by(New.title).all()
        return render_template("search.html", form=form,
            searched= new.searched, news=news)

@bp.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@bp.route('/date')
def get_current_date():
    return {"Date": date.today()}

#Custom error pages

#Invalid URL
@bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal Server
@bp.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

#Create Name Page
@bp.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = UserForm()
    #validate
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Submission successful!")
    
    return render_template("name.html",
        name = name,
        form = form)

#Create PSW TEST
@bp.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    #validate
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        #clear
        form.email.data = ''
        form.password_hash.data = ''
        #index user by email
        pw_to_check = User.query.filter_by(email=email).first()
        #check hashed pw
        passed = check_password_hash(pw_to_check.password_hash, password)
    
    return render_template("test_pw.html",
        email = email,
        password= password,
        form=form,
        pw_to_check=pw_to_check,
        passed=passed)