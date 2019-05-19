from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from flask import url_for
from app import db


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120),unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    registered_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    api_token = db.Column(db.String(120),unique=True)
    votes = db.relationship('Vote', backref='giver', lazy='dynamic')
    videos = db.relationship('Video', backref='uploader', lazy='dynamic')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def VotedOnVideo(self,video_id):
        return Vote.query.filter_by(user_id=self.id,video_id=video_id).count()>0
    
    def voteOnVideo(self,video_id):
        if self.VotedOnVideo(video_id):
            return False
        vote = Vote(user_id=self.id,video_id=video_id)
        db.session.add(vote)
        db.session.commit() 
        return 1
    
    def takeVoteBack(self,video_id):
        Vote.query.filter_by(user_id=self.id,video_id=video_id).delete()
        db.session.commit()
        return 1

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    text = db.Column(db.String(2048))
    image_url = db.Column(db.String(265))
    video_url = db.Column(db.String(256))
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    votes = db.relationship('Vote', backref='video', lazy='dynamic')

    def getStateString(self):
        if self.is_published:
            return 'Published'
        else:
            return 'Hidden'
    def getImgagePublicUrl(self):
        return url_for('uploaded_images_access',filename=self.image_url)
    def getVideoPulbicUrl(self):
        return url_for('uploaded_videos_access',filename=self.video_url)




class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
