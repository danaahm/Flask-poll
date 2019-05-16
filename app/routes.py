from flask import render_template, flash, redirect, url_for,send_from_directory
from app import app
from app.forms import LoginForm
from app.forms import RegisterForm
from app.forms import SubmitVideoForm
from flask_login import current_user, login_user,logout_user
from app.models import User,Video
from app import db
import os
import os.path
import uuid
from werkzeug.utils import secure_filename

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
		return redirect(url_for('login'))
	return render_template("dashboard.html")

@app.route('/admin/users')
def users():
	if not (current_user.is_authenticated and current_user.is_admin):
		return redirect(url_for('login'))
	users= User.query.filter_by(is_admin=False)
	return render_template("users.html",users=users)

@app.route('/admin/users/delete/<user_id>')
def delete_user(user_id):
	if not (current_user.is_authenticated and current_user.is_admin):
		return redirect(url_for('users'))
	user = User.query.filter_by(id=user_id).first()
	flash("User "+user.email+" Has been Removed!")
	User.query.filter_by(id=user_id).delete()
	db.session.commit()
	return redirect(url_for('users'))

@app.route('/admin/videos')
def videos():
	if not (current_user.is_authenticated and current_user.is_admin):
		return redirect(url_for('users'))
	videos = Video.query.all()
	return render_template("videos.html",videos=videos)

@app.route('/admin/videos/new',methods=['GET', 'POST'])
def admin_new_video():
	if not (current_user.is_authenticated and current_user.is_admin):
		return redirect(url_for('login'))
	form = SubmitVideoForm()
	if form.validate_on_submit():
		f1 = form.image.data
		f2 = form.video.data
		ext1 = os.path.splitext(f1.filename)[1]
		ext2 = os.path.splitext(f2.filename)[1]
		filename1 = str(uuid.uuid4())+ext1
		filename2 = str(uuid.uuid4())+ext2
		f1.save(os.path.join(app.images_upload_dir,filename1))
		f2.save(os.path.join(app.videos_upload_dir,filename2))
		
		video = Video(title=form.title.data,text=form.text.data,image_url=filename1,video_url=filename2,is_published=True,uploaded_by=current_user.id)
		db.session.add(video)
		db.session.commit()
		flash('Video submited')
		return redirect(url_for('videos'))
	return render_template('admin_new_video.html', title='Submit new video', form=form)


@app.route('/submit')
def submit():
	return render_template("submit_video.html")

@app.route('/view')
def view():
	return render_template("view_video.html")









@app.route('/votes')
def votes():
	return render_template("votes.html")




#serve uploaded images and videos
@app.route('/uploads/images/<filename>')
def uploaded_images_access(filename):
	return send_from_directory(app.images_upload_dir,filename) 

@app.route('/uploads/videos/<filename>')
def uploaded_videos_access(filename):
	return send_from_directory(app.videos_upload_dir,filename) 
