from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from config import Config

from models import User
from models import db

app = Flask(__name__)
app.config.from_object(Config)
#app.config["SQLALCHEMY_DATABASE_URI"] = database_directory

#db = SQLAlchemy(app)

db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
	# 1. Fetch against the database a user by `id` 
    # 2. Create a new object of `User` class and return it.
	return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
	return redirect('/login')

@app.route('/signup',methods=['GET','POST'])
def signup():

	if current_user is not None:
		logout_user()
	if request.method == 'POST':
		credentials = request.form
		if credentials_taken(credentials):

			cred_tup = valid_credentials(credentials)
			if not cred_tup[0]:
				return render_template('signup.html',error=cred_tup[1])


			#hash password
			hashed_password = generate_password_hash(credentials['password'], method='sha256')

			#this is an object model
			new_user = User(username=credentials['username'],password=hashed_password)
			db.session.add(new_user)
			db.session.commit()


			#return new user page?
			return log_the_user_in(new_user.username)
		else:
			return render_template('signup.html',error="Username taken. Please choose another username.")


	return render_template('signup.html')


def valid_credentials(credentials):
	#username valid one special character or number O(n) time
	username = credentials['username']
	password = credentials['password']

	err1 = "Password must be at least 7 characters with a number or special character"
	err2 = "Username must be at least 7 characters"
	err3 = "Must have a number or special character in password."

	if len(username) < 7:
		return False, err2

	if len(password) < 7:
		return False, err1

	for i in range(len(password)):
		if password[i].isdigit():
			return True, ""
		if password[i] in ['~','!','@','#','$','%','^','&','*']:
			return True, ""
			
	return False, err3


def credentials_taken(credentials):
	#username not taken secure etc
	if User.query.filter_by(username=credentials['username']).first():
		print("username taken")
		return False
	else:
		return True


@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = ''
	if request.method == 'POST':
		if valid_login(request.form['username'], request.form['password']):
			return log_the_user_in(request.form['username'])
		else:
			error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
	return render_template('signin.html', error=error)

def valid_login(user, passwd):

	user_result = User.query.filter_by(username=user).first()

	if user_result:
		#check if the hashes match
		if check_password_hash(user_result.password,passwd):
			return True
	return False


def log_the_user_in(user):
	user_inst = User.query.filter_by(username=user).first()
	print(user_inst)
	#user_inst should be an instance of  User class
	login_user(user_inst)

	return redirect(url_for('home'))
	
def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app


    '''
    from config import Config
	from app import db, create_app
	db.create_all(app=create_app(Config))
	'''

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
	return render_template('index.html')

@app.route('/')
def index():
	return redirect('/home')

#@app.route('/profile')



#so task queues are for long running jobs not suited for request/response cycle. Manage background work.
#could use cron jobs apparently. Checking out celery and redis.


if __name__ == "__main__":
	app.run()
	

