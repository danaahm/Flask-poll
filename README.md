# Flask Poll Application: Best EPL Goal of the 18/19 Season

A web polling application written with Python (Flask) that allows users to vote on and create voting options of the best EPL goal of the 18/19 season. Users will be prompted with a poll question and related options. They can vote on option(s) and see poll results. Poll results are then loaded into an internal DB based on sqlite. Users have the ability to upload a new poll option, including a video in web format, a icon picture, title and description. Admin can then approve and post these submissions.

##Design and development

Both authors are association football fans and decided a poll for the best goal of the past season would be interesting. We used bootstrap and boilerplate to get us started and then built our flask application based off of the Flask mega tutorial (mainly flask login, and then integrated with flask admin). Then looked to Flask uploads for the uploading of videos and images to our application. Dana focused mainly on front-end and Nicole on back-end.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What you need to install the software

```
pip install -r requirements.txt
```

### Installing

This application can be deployed locally. On linux, install git and clone the reposistory.

Get the code:
```
git clone https://github.com/danaahm/Flask-poll
```
How to run from zip

Generate a virtual environment and install dependencies:
```
Unix:
$ python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Windows:
$ venv\Scripts\activate
(venv) $ _
pip install -r requirements.txt
```

set the FLASK_APP and FLASK_DEBUG variables
```
export FLASK_APP=polling.py
export FLASK_DEBUG=1
```

Initialise database

```
flask db migrate
flask db upgrade
```

Start the application:
```
flask run polling.py
Check if a poll already exists into db
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```


If you run the application with app.db and the current migrations, there are logins that
demonstrate the applications functionality.

Admin login:
```
admin@domain.com
password: 123
```
User login:
```
user@domain.com
password: 246
```

### Coding style tests

HTML and CSS have been validated using w3schools validator:

```
https://validator.w3.org/#validate_by_uri
```

## Deployment

To deploy on Heroku, visit heroku.com and create a free account.
Once the CLI is installed is login to your Heroku account:

```
$ heroku login
```

HerokuCLI will ask you to enter your email address and your account password.
Git must be installed on your system for deployment.

To register a new application, use the apps:create command :
```
$ heroku apps:create Flask-poll-master
```

Change config log (config.py) and init (__init__.py) for application to log directly to standard output.
```
class Config(object):
    # ...
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
```
```
if app.config['LOG_TO_STDOUT']:
```
Set the LOG_TO_STDOUT environment variable when the application runs in Heroku:
```
$ heroku config:set LOG_TO_STDOUT=1
```

Create a file named Procfile in the root directory of the application:
```
web: flask db upgrade; flask translate compile; gunicorn Flask-poll-master:app
```
Add the FLASK_APP environment variable:
```
$ heroku config:set FLASK_APP=polling.py
```

Upload the application to Heroku's servers for deployment, using the git push command.
```
$ git checkout -b deploy
$ git push heroku deploy:master
```

```
$ git commit -a -m "heroku deployment changes"
```
Start the deployment:
```
$ git push heroku master
```

## Built With

* [Flask](http://flask.pocoo.org/) - Web framework
* [Bootstrap](https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css) - CSS stylesheet
* [JQuery](https://code.jquery.com/jquery-3.2.1.slim.min.js)- JS library
* [CDNJS](https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js)- JS library

#Image and Video content
* https://www.youtube.com/watch?v=I9vXpswxMRk Chelsea Sturridge goal
* http://www.soccer-blogger.com/2019/01/12/gif-video-andre-schurrle-goal-vs-burnley-2019-fantastic-schurrle-volley-for-fulham/ Fulham Schurrle goal
* https://www.youtube.com/watch?v=qn2sW-3LpmA Leicester Sigurdsson goal
* https://i2.wp.com/static1.businessinsider.com/image/572d8464dd08956c3e8b4586-1190-625/the-18-biggest-soccer-stadiums-in-the-world.jpg Index banner image
* https://lh3.googleusercontent.com/7w4hDxi9fkOqDSxLzW5_CxZmWqzrq7PNzYxYncT2thdcMN9pgF7I0JawWI1jLHbcYd5sLw=s151 Goal image

## Versioning

For the versions available, see the git repository (https://github.com/danaahm/Flask-poll).

## Authors

* **Nicole Low & Dana Ahmadi** -

See also (https://github.com/danaahm/Flask-poll/contributors) via Github, or git log .txt file.

## Acknowledgments
* Miguel Grinberg for his Flask mega tutorial, used as a basis for our code (https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) and for information on Heroku Deployment
* https://github.com/danidee10/Votr used as reference on how to build a Flask poll/inspiration
* https://github.com/kalise/flask-vote-app used as reference on how to build a Flask poll/inspiration
* https://github.com/hemepositive/flask-polls used as reference on how to build a Flask poll/inspiration
* https://github.com/maxcountryman/flask-login used as further reference on user logins
* https://github.com/realpython/flask-boilerplate used as our first boilerplate
* https://github.com/joshfriend/flask-restful-demo used as reference/inspiration for RESTful API
