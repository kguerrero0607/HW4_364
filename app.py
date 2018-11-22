# An application in Flask where you can log in and create user accounts to save Gif collections
# SI 364 - F18 - HW4

# TODO 364: Check out the included file giphy_api_key.py and follow the instructions in TODOs there before proceeding to view functions.

# TODO 364: All templates you need are provided and should not be edited. However, you will need to inspect the templates that exist in order to make sure you send them the right data!

# Import statements
import os
import requests
import json
from giphy_api_key import api_key
from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash

# Imports for login management
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/HW4db" # TODO 364: You should edit this to correspond to the database name YOURUNIQNAMEHW4db and create the database of that name (with whatever your uniqname is; for example, my database would be jczettaHW4db). You may also need to edit the database URL further if your computer requires a password for you to run this.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# App addition setups
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# Login configurations setup
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app) # set up login manager

########################
######## Models ########
########################

## Association tables
# NOTE - 364: You may want to complete the models tasks below BEFORE returning to build the association tables! That will making doing this much easier.

# NOTE: Remember that setting up association tables in this course always has the same structure! Just make sure you refer to the correct tables and columns!

# TODO 364: Set up association Table between search terms and GIFs (you can call it anything you want, we suggest 'tags' or 'search_gifs').



# TODO 364: Set up association Table between GIFs and collections prepared by user (you can call it anything you want. We suggest: user_collection)



## User-related Models

# Special model for users to log in
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    #TODO 364: In order to complete a relationship with a table that is detailed below (a one-to-many relationship for users and gif collections), you'll need to add a field to this User model. (Check out the TODOs for models below for more!)
    # Remember, the best way to do so is to add the field, save your code, and then create and run a migration!

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

## DB load function
## Necessary for behind the scenes login manager that comes with flask_login capabilities! Won't run without this.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # returns User object or None

# TODO 364: Read through all the models tasks before beginning them so you have an understanding of what the database structure should be like. Consider thinking about it as a whole and drawing it out before you write this code.

# Model to store gifs
class Gif(db.Model):
    pass # Replace with code
    # TODO 364: Add code for the Gif model such that it has the following fields:
    # id (Integer, primary key)
    # title (String up to 128 characters)
    # embedURL (String up to 256 characters)

    # TODO 364: Define a __repr__ method for the Gif model that shows the title and the URL of the gif

# Model to store a personal gif collection
class PersonalGifCollection(db.Model):
    pass
    # TODO 364: Add code for the PersonalGifCollection model such that it has the following fields:
    # id (Integer, primary key)
    # name (String, up to 255 characters)

    # This model should have a one-to-many relationship with the User model (one user, many personal collections of gifs with different names -- say, "Happy Gif Collection" or "Sad Gif Collection")

    # This model should also have a many to many relationship with the Gif model (one gif might be in many personal collections, one personal collection could have many gifs in it).

class SearchTerm(db.Model):
    pass
    # TODO 364: Add code for the SearchTerm model such that it has the following fields:
    # id (Integer, primary key)
    # term (String, up to 32 characters, unique) -- You want to ensure the database cannot save non-unique search terms
    # This model should have a many to many relationship with gifs (a search will generate many gifs to save, and one gif could potentially appear in many searches)

    # TODO 364: Define a __repr__ method for this model class that returns the term string


########################
######## Forms #########
########################

# Provided
class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    username = StringField('Username:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    #Additional checking methods for the form
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

# Provided
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

# TODO 364: The following forms for searching for gifs and creating collections are provided and should not be edited. You SHOULD examine them so you understand what data they pass along and can investigate as you build your view functions in TODOs below.
class GifSearchForm(FlaskForm):
    search = StringField("Enter a term to search GIFs", validators=[Required()])
    submit = SubmitField('Submit')

class CollectionCreateForm(FlaskForm):
    name = StringField('Collection Name',validators=[Required()])
    gif_picks = SelectMultipleField('GIFs to include')
    submit = SubmitField("Create Collection")

########################
### Helper functions ###
########################

def get_gifs_from_giphy(search_string):
    """ Returns data from Giphy API with up to 5 gifs corresponding to the search input"""
    baseurl = "https://api.giphy.com/v1/gifs/search"
    pass # Replace with code
    # TODO 364: This function should make a request to the Giphy API using the input search_string, and your api_key (imported at the top of this file)
    # Then the function should process the response in order to return a list of 5 gif dictionaries.
    # HINT: You'll want to use 3 parameters in the API request -- api_key, q, and limit. You may need to do a bit of nested data investigation and look for API documentation.
    # HINT 2: test out this function outside your Flask application, in a regular simple Python program, with a bunch of print statements and sample invocations, to make sure it works!

# Provided
def get_gif_by_id(id):
    """Should return gif object or None"""
    g = Gif.query.filter_by(id=id).first()
    return g

def get_or_create_gif(title, url):
    """Always returns a Gif instance"""
    pass # Replace with code
    # TODO 364: This function should get or create a Gif instance. Determining whether the gif already exists in the database should be based on the gif's title.

def get_or_create_search_term(term):
    """Always returns a SearchTerm instance"""
    # TODO 364: This function should return the search term instance if it already exists.

    # If it does not exist in the database yet, this function should create a new SearchTerm instance.

    # This function should invoke the get_gifs_from_giphy function to get a list of gif data from Giphy.

    # It should iterate over that list acquired from Giphy and invoke get_or_create_gif for each, and then append the return value from get_or_create_gif to the search term's associated gifs (remember, many-to-many relationship between search terms and gifs, allowing you to do this!).

    # If a new search term were created, it should finally be added and committed to the database.
    # And the SearchTerm instance that was got or created should be returned.

    # HINT: I recommend using print statements as you work through building this function and use it in invocations in view functions to ensure it works as you expect!

def get_or_create_collection(name, current_user, gif_list=[]):
    """Always returns a PersonalGifCollection instance"""
    pass # Replace with code

    # TODO 364: This function should get or create a personal gif collection. Uniqueness of the gif collection should be determined by the name of the collection and the id of the logged in user.

    # In other words, based on the input to this function, if there exists a collection with the input name, associated with the current user, then this function should return that PersonalGifCollection instance.

    # However, if no such collection exists, a new PersonalGifCollection instance should be created, and each Gif in the gif_list input should be appended to it (remember, there exists a many to many relationship between Gifs and PersonalGifCollections).
    # HINT: You can think of a PersonalGifCollection like a Playlist, and Gifs like Songs.



########################
#### View functions ####
########################

## Error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


## Login-related routes - provided
@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/secret')
@login_required
def secret():
    return "Only authenticated users can do this! Try to log in or contact the site admin."

## Other routes
@app.route('/', methods=['GET', 'POST'])
def index():
    # TODO 364: Edit this view function, which has a provided return statement, so that the GifSearchForm can be rendered.
    # If the form is submitted successfully:
    # invoke get_or_create_search_term on the form input and redirect to the function corresponding to the path /gifs_searched/<search_term> in order to see the results of the gif search. (Just a couple lines of code!)

    # HINT: invoking url_for with a named argument will send additional data. e.g. url_for('artist_info',artist='solange') would send the data 'solange' to a route /artist_info/<artist>
    return render_template('index.html',form=form)

# Provided
@app.route('/gifs_searched/<search_term>')
def search_results(search_term):
    term = SearchTerm.query.filter_by(term=search_term).first()
    relevant_gifs = term.gifs.all()
    return render_template('searched_gifs.html',gifs=relevant_gifs,term=term)

@app.route('/search_terms')
def search_terms():
    pass # Replace with code
    # TODO 364: Edit this view function so it renders search_terms.html.
    # That template should show a list of all the search terms that have been searched so far. Each one should link to the gifs that resulted from that search.
    # HINT: All you have to do is make the right query in this view function and send the right data to the template! You can complete this in two lines. Check out the template for more hints!

# Provided
@app.route('/all_gifs')
def all_gifs():
    gifs = Gif.query.all()
    return render_template('all_gifs.html',all_gifs=gifs)

@app.route('/create_collection',methods=["GET","POST"])
@login_required
def create_collection():
    form = CollectionCreateForm()
    gifs = Gif.query.all()
    choices = [(g.id, g.title) for g in gifs]
    form.gif_picks.choices = choices
    # TODO 364: If the form validates on submit, get the list of the gif ids that were selected from the form. Use the get_gif_by_id function to create a list of Gif objects.  Then, use the information available to you at this point in the function (e.g. the list of gif objects, the current_user) to invoke the get_or_create_collection function, and redirect to the page that shows a list of all your collections.
    # If the form is not validated, this view function should simply render the create_collection.html template and send the form to the template.


@app.route('/collections',methods=["GET","POST"])
@login_required
def collections():
    pass # Replace with code
    # TODO 364: This view function should render the collections.html template so that only the current user's personal gif collection links will render in that template. Make sure to examine the template so that you send it the correct data!

# Provided
@app.route('/collection/<id_num>')
def single_collection(id_num):
    id_num = int(id_num)
    collection = PersonalGifCollection.query.filter_by(id=id_num).first()
    gifs = collection.gifs.all()
    return render_template('collection.html',collection=collection, gifs=gifs)

if __name__ == '__main__':
    db.create_all()
    manager.run()
