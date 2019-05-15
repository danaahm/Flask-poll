from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from app.forms import RegisterForm
from flask_login import current_user, login_user,logout_user
from app.models import User
from app import db

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/register',methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, True)
		if user.is_admin:
			return redirect(url_for('dashboard'))
		else:
			return redirect(url_for('index'))

	return render_template('login.html', title='Log in', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/admin/dashboard')
def dashboard():
	if not (current_user.is_authenticated and current_user.is_admin):
		return redirect(url_for('index'))
	return render_template("dashboard.html")

@app.route('/admin/users')
def users():
	if not (current_user.is_authenticated and current_user.is_admin):
		return redirect(url_for('index'))
	return render_template("users.html")

@app.route('/submit')
def submit():
	return render_template("submit_video.html")

@app.route('/view')
def view():
	return render_template("view_video.html")








@app.route('/votes')
def votes():
	return render_template("votes.html")

@app.route('/videos')
def videos():
	return render_template("videos.html")
