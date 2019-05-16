from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '42d62eb7d5291eeba627863ca158d84b6cf63b32';
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

#Upload config
app.upload_dir = os.path.join(basedir, 'uploads')
app.images_upload_dir = os.path.join(app.upload_dir, 'images')
app.videos_upload_dir = os.path.join(app.upload_dir, 'videos')

app.config['UPLOADED_IMAGES_DEST'] = app.images_upload_dir


images = UploadSet('images', IMAGES)
configure_uploads(app, (images,))

from app import routes, models