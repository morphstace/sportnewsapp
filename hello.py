from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def index():

    example_list = [21, "ciao", "esempio"]
    return render_template("index.html", example_list=example_list) 

@app.route('/user/<name>')

def user(name):
    #return "TEST"
    return render_template("user.html", name=name)

#Custom error pages

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal Server
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500