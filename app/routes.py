from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'MiguwSel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/submit')
def submit():
	return render_template("submit_video.html")

@app.route('/view')
def view():
	return render_template("view_video.html")

@app.route('/login')
def login():
	return render_template("login.html")

@app.route('/dash')
def dash():
	return render_template("dashboard.html")

@app.route('/users')
def users():
	return render_template("users.html")


@app.route('/votes')
def votes():
	return render_template("votes.html")

@app.route('/videos')
def videos():
	return render_template("videos.html")
