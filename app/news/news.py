from app.news import bp
from flask import render_template, redirect, url_for, flash
from app.models import Users, News
from app.forms import NewsForm, UserForm, PasswordForm, SearchForm
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash
from app.extensions import db
from datetime import date


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/news/<int:id>')
def new(id):
    new = News.query.get_or_404(id)
    return render_template('new.html', new=new)

@bp.route('/news/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_new(id):
    new = News.query.get_or_404(id)
    form = NewsForm()
    if form.validate_on_submit():
        new.title = form.title.data
        new.slug = form.slug.data
        new.content = form.content.data
        db.session.add(new)
        db.session.commit()
        flash("Update successfull!")
        return redirect(url_for('news.new', id=new.id))
    if current_user.id == new.poster_id:
        form.title.data = new.title
        form.slug.data = new.slug
        form.content.data = new.content
        return render_template('edit_new.html', form=form)
    flash("You are not authorized to edit.")
    return render_template('new.html', new=new)
    

@bp.route('/add-news', methods=['GET','POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        poster = current_user.id
        news = News(title=form.title.data, content=form.content.data, 
            poster_id=poster, slug=form.slug.data)
        form.title.data=''
        form.content.data=''
        form.slug.data=''

        db.session.add(news)
        db.session.commit()

        flash("News submitted successfully!")
    return render_template("add_news.html", form=form)

@bp.route('/news/delete/<int:id>')
@login_required
def delete_new(id):
    new_to_del = News.query.get_or_404(id)
    id = current_user.id
    if id == new_to_del.poster.id:
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
    news = News.query.order_by(News.date_posted)
    return render_template("news.html", news=news)

@bp.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    news = News.query
    if form.validate_on_submit():
        new.searched = form.searched.data
        news = news.filter(News.content.like('%'+new.searched+'%'))
        news = news.order_by(News.title).all()
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
        pw_to_check = Users.query.filter_by(email=email).first()
        #check hashed pw
        passed = check_password_hash(pw_to_check.password_hash, password)
    
    return render_template("test_pw.html",
        email = email,
        password= password,
        form=form,
        pw_to_check=pw_to_check,
        passed=passed)