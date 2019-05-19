from flask import render_template, flash, redirect, url_for,send_from_directory,jsonify,request
from app import app
from app.forms import LoginForm
from app.forms import RegisterForm
from app.forms import SubmitVideoForm
from app.forms import EditVideoForm
from flask_login import current_user, login_user,logout_user
from app.models import User,Video,Vote
from app import db
import os
import os.path
import uuid
from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/index')
def index():
	def func(vid):
		return vid.votes.count()
	videos = sorted(Video.query.filter_by(is_published=True),key=func,reverse=True)
	first = videos[0]

	video_3_per_row = [[]]
	index = 0
	for v in videos:
		if len(video_3_per_row[-1]) < 3:
			video_3_per_row[-1].append(index)
		else:
			video_3_per_row.append([index])
		index += 1

		
			
	return render_template('index.html', title='Home',videos=videos,first=first,video_3_per_row=video_3_per_row)

@app.route('/register',methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,api_token=str(uuid.uuid4()))
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
	def func(vid):
		return vid.votes.count()
	videos = sorted(Video.query.all(),key=func,reverse=True)
	return render_template("dashboard.html",videos=videos)

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
	Vote.query.filter_by(user_id=user_id).delete()
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



@app.route('/view/<video_id>')
def view(video_id):
	video = Video.query.filter_by(id=video_id).first()
	if video.is_published == False and current_user.is_admin == False:
		return redirect(url_for('index'))
	return render_template("view_video.html",video=video)

@app.route('/videos/<video_id>/<action>')
def video_action(video_id,action):
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	if (action=='publish' or action=='unpublish' or action=='delete') and current_user.is_admin == False:
		return redirect(url_for('login'))

	video = Video.query.filter_by(id=video_id).first()
	
	if action=='publish':
		video.is_published = True
		db.session.commit()
		return redirect(url_for('videos'))
	
	if action=='unpublish':
		video.is_published = False
		db.session.commit()
		return redirect(url_for('videos'))
	if action=='delete':
		Vote.query.filter_by(video_id=video.id).delete()
		db.session.delete(video)
		db.session.commit()
		return redirect(url_for('videos'))

	
	if action=='vote':
		current_user.voteOnVideo(video.id)
		return redirect(url_for('view',video_id=video.id))
	
	if action=='takebakvote':
		current_user.takeVoteBack(video.id)
		return redirect(url_for('view',video_id=video.id))
	
	return redirect(url_for('index'))
	

@app.route('/videos/<video_id>/edit',methods=['GET', 'POST'])
def edit_video(video_id):
	if not (current_user.is_authenticated and current_user.is_admin):
		return redirect(url_for('login'))

	video = Video.query.filter_by(id=video_id).first()

	form = EditVideoForm()
	
	if form.validate_on_submit():
		video.title = form.title.data
		video.text = form.text.data
		
		if form.image.data:
			f1 = form.image.data
			ext1 = os.path.splitext(f1.filename)[1]
			filename1 = str(uuid.uuid4())+ext1
			f1.save(os.path.join(app.images_upload_dir,filename1))
			video.image_url=filename1
		if form.video.data:
			f2 = form.video.data
			ext2 = os.path.splitext(f2.filename)[1]
			filename2 = str(uuid.uuid4())+ext2
			f2.save(os.path.join(app.videos_upload_dir,filename2))
			video.video_url=filename2
		db.session.commit()
		flash('Video updated')
		return redirect(url_for('videos'))
	else:
		form.title.data = video.title
		form.text.data = video.text
	return render_template('admin_new_video.html', title='Edit Video', form=form)


	

		

@app.route('/submit',methods=['GET', 'POST'])
def submit():
	if not (current_user.is_authenticated):
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
		
		video = Video(title=form.title.data,text=form.text.data,image_url=filename1,video_url=filename2,is_published=False,uploaded_by=current_user.id)
		db.session.add(video)
		db.session.commit()
		flash('Video submited')
		return redirect(url_for('index'))
	return render_template('submit_video.html', title='Submit new video', form=form)
	








@app.route('/votes')
def votes():
	votes = Vote.query.all()
	return render_template("votes.html",votes=votes)




#serve uploaded images and videos
@app.route('/uploads/images/<filename>')
def uploaded_images_access(filename):
	return send_from_directory(app.images_upload_dir,filename) 

@app.route('/uploads/videos/<filename>')
def uploaded_videos_access(filename):
	return send_from_directory(app.videos_upload_dir,filename) 

#####################
#API routes for users
#####################
def get_api_user():
	if not 'token' in request.headers:
		return None
	users = User.query.filter_by(api_token=request.headers['token'])
	if users.count()>0:
		return users[0]
	else:
		return None


@app.route('/api/homepage')
def api_homepage():
	def func(vid):
		return vid.votes.count()
	videos = sorted(Video.query.filter_by(is_published=True),key=func,reverse=True)

	vids = []
	i = 1
	for v in videos:
		vids.append({'id':v.id,'title':v.title,'votes':v.votes.count(),'rank':i})
		i += 1
	return jsonify({'success':True,'data':vids})


@app.route('/api/video/<video_id>')
def api_get_video(video_id):
	user = get_api_user()
	videos = Video.query.filter_by(id=video_id)
	if videos.count()==0:
		return jsonify({'success':False,'message':'invalid id.'})
	else:
		v = {}
		v['id'] = video_id
		v['title'] = videos[0].title
		v['text'] = videos[0].text
		v['image'] = videos[0].getImgagePublicUrl()
		v['video'] = videos[0].getVideoPulbicUrl()
		if user:
			v['you_voted']= user.VotedOnVideo(video_id)
		return jsonify({'success':True,'data':v})
		
		
	

@app.route('/api/video/<video_id>/vote',methods=['POST','DELETE'])
def api_vote(video_id):
	user = get_api_user()
	if not user:
		return jsonify({'success':False,'message':'invalid token.'})
	
	if request.method == 'POST':
		user.voteOnVideo(video_id)
	if request.method == 'DELETE':
		user.takeVoteBack(video_id)

	return jsonify({'success':True})


#####################
#API routes for admin
#####################

@app.route('/api/admin/users')
def api_admin_get_users():
	user = get_api_user()
	if not (user and user.is_admin):
		return jsonify({'success':False,'message':'invalid token.'})

	users = User.query.filter_by(is_admin=False)
	us = []
	for u in users:
		us.append({'id':u.id,'email':u.email,'registered_at':u.registered_at})
	return jsonify({'success':True,'data':us})
	



@app.route('/api/admin/user/<user_id>',methods=['DELETE'])
def api_admin_remove_user(user_id):
	user = get_api_user()
	if not (user and user.is_admin):
		return jsonify({'success':False,'message':'invalid token.'})

	user = User.query.filter_by(id=user_id).delete()
	Vote.query.filter_by(user_id=user_id).delete()
	db.session.commit()
	return jsonify({'success':True})

@app.route('/api/admin/votes')
def api_admin_get_votes():
	user = get_api_user()
	if not (user and user.is_admin):
		return jsonify({'success':False,'message':'invalid token.'})

	votes = Vote.query.all()
	vs = []
	for v in votes:
		vs.append({'id':v.id,'user_id':v.user_id,'video_id':v.video_id,'timestamp':v.timestamp})
	return jsonify({'success':True,'data':vs})
	


@app.route('/api/admin/vote/<vote_id>',methods=['DELETE'])
def api_admin_remove_vote(vote_id):
	user = get_api_user()
	if not (user and user.is_admin):
		return jsonify({'success':False,'message':'invalid token.'})

	user = Vote.query.filter_by(id=vote_id).delete()
	db.session.commit()
	return jsonify({'success':True})	


@app.route('/api/admin/videos')
def api_admin_get_videos():
	user = get_api_user()
	if not (user and user.is_admin):
		return jsonify({'success':False,'message':'invalid token.'})

	videos = Video.query.all()
	vs = []
	for v in videos:
		vs.append({'id':v.id,'title':v.title,'votes':v.votes.count(),'uploaded_by':v.uploaded_by,'is_published':v.is_published})
	return jsonify({'success':True,'data':vs})

@app.route('/api/admin/video/<video_id>',methods=['DELETE'])
def api_admin_remove_video(video_id):
	user = get_api_user()
	if not (user and user.is_admin):
		return jsonify({'success':False,'message':'invalid token.'})

	Video.query.filter_by(id=video_id).delete()
	Vote.query.filter_by(video_id=video_id).delete()
	db.session.commit()

	return jsonify({'success':True})	


@app.route('/api/admin/video/<action>/<video_id>',methods=['POST'])
def api_admin_video_action(action,video_id):
	user = get_api_user()
	if not (user and user.is_admin):
		return jsonify({'success':False,'message':'invalid token.'})

	videos = Video.query.filter_by(id=video_id)

	if videos.count()==0:
		return jsonify({'success':False,'message':'invalid id.'})
	
	if action=='publish':
		videos[0].is_published = True
	elif action=='unpublish':
		videos[0].is_published = False
	else:
		return jsonify({'success':False,'message':'invalid action '+action})

	
	
	db.session.commit()
	return jsonify({'success':True})	
	










