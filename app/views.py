from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, twit
import tweepy
from .forms import LoginForm, RegisterForm, PostForm, TweetsForm
from .models import User, Post

# -- user functions -- #

# given a user_id, returns associated User instance
@lm.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


# executes at the beginning of a request chain
# we use this to store information about the user when the request began
@app.before_request
def before_request():
    g.user = current_user # global of Flask Login

# -- #


# home page can be seen by anyone
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    posts = Post.query.all() # grabbing all posts to display on the home page
    form = PostForm(request.form)
    # upon seeing valid data
    if request.method == 'POST' and form.validate():
    	db.metadata.create_all(db.engine)
    	# create a new post
    	post = Post(body=form.body.data,
    	            author_username=g.user.username)
    	# add it to the database
    	db.session.add(post)
    	db.session.commit()
        return redirect(url_for('index'))
    return render_template("index.html",
                           title='Home',
                           user=g.user,
                           form=form,
                           posts=posts)

@app.route('/user_info')
def user_info():
	users = User.query.all()
	return render_template("user_info.html",
		                    title='User Information',
		                    users=users)

# This route is similar in structure to the following login route
@app.route('/register', methods=['GET', 'POST'])
def register():
	# if the user is already logged into a valid account
    if (g.user is not None and g.user.is_authenticated):
        return redirect(url_for('index'))
    # otherwise
    form = RegisterForm(request.form)
    # upon seeing valid data
    if request.method == 'POST' and form.validate():
    	# here, we would check if the user already exists and act accordingly
    	# then, if not, create the user and log them in
    	db.metadata.create_all(db.engine)
        user = User(username=form.username.data,
                    password=form.password.data, # warning!
                                                 # the password isn't encrypted!
                    )
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=False)
        return redirect(url_for('index'))
    return render_template('register.html', 
                           title='Create a New Account',
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if the user is already logged in to a valid account
    if (g.user is not None and g.user.is_authenticated):
        return redirect(url_for('index'))
    # otherwise
    form = LoginForm()
    if request.method == 'POST' and form.validate():
    	user = user_loader(form.username.data)
        if user:
            if user.password == form.password.data:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('index'))
    return render_template('login.html', 
                           title='Sign In',
                           form=form)

# if the user is logged in, log them out
@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('index'))

# Allows a registered user to search for tweets with keywords
@app.route('/search_twitter', methods=['GET', 'POST'])
@login_required
def search_twitter():
    form = TweetsForm()
    num_tweets = 15
    tweets = None
    if request.method == 'POST' and form.validate():
        tweets = twit.collect_tweets_from_query(form.search_tag.data,
                                                num_tweets)
    return render_template('search_tweets.html', 
                           title='Search Twitter',
                           form=form,
                           tweets=tweets)

