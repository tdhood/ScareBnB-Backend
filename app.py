from csv import unregister_dialect
from email.base64mime import header_encode
from email.headerregistry import ContentTypeHeader
import os
from dotenv import load_dotenv

from flask import Flask, jsonify, render_template, request, flash, redirect, json
from flask_debugtoolbar import DebugToolbarExtension

from forms import ListingAddForm, UserAddForm, LoginForm
from models import db, connect_db, User, Listing
from aws import upload_file
from botocore.exceptions import ClientError


import jwt

load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
print(os.environ['DATABASE_URL'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

connect_db(app)

# BASE_IMAGE_URL = 'https://share-b-n-b.s3.us-west-1.amazonaws.com/'

#############################################################################
# User signup/login/logout



#for reference, since we plan to serve front-end through react
# most likely wont use or need these
# @app.before_request
# def add_user_to_g():
#     """If we're logged in, add curr user to Flask global."""

#     if CURR_USER_KEY in session:
#         g.user = User.query.get(session[CURR_USER_KEY])

#     else:
#         g.user = None

# api won't track login status
# def do_login(user):
#     """Log in user."""

#     session[CURR_USER_KEY] = user.id

# api won't track login status
# def do_logout():
#     """Log out user."""

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    print('signup route')
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    # if CURR_USER_KEY in session:
    #     del session[CURR_USER_KEY]
    received = request.json
    print('received', received)
    form = UserAddForm(csrf_enabled=False, data=received)
    print('form=', form)
    print("username", received["username"])
    print('password', received["password"])

    if form.validate_on_submit():
        username = received["username"]
        password = received["password"]
        email = received["email"]
        first_name = received["first_name"]
        last_name = received["last_name"]
        bio = received["bio"]
        is_host = False
        print("username", username)

        try:
            user = User.signup(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                bio=bio,
                is_host=is_host,
                # image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

            serialized = user[0].serialize()
        
            return jsonify(user=serialized, token=user[1]) 

        except ClientError as e:
            #TODO: default image
            return jsonify(e)
        
    return jsonify(errors=form.errors)

        
    

# @app.route('/register', methods=['GET', 'POST'])
# def signup_user():
#  data = request.get_json()

#  hashed_password = generate_password_hash(data['password'], method='sha256')

#  new_user = Users( 
#     first_name=data['first name'], 
#     password=hashed_password, 
#     is_host=False)
#  db.session.add(new_user)
#  db.session.commit()

#  return jsonify({'message': 'registered successfully'})

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login and redirect to homepage on success."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.post('/logout')
def logout():
    """Handle logout of user and redirect to homepage."""

    if CURR_USER_KEY in session:
        form = g.csrf_form

        if form.validate_on_submit():
            do_logout()
            flash("You've been logged out")

    return redirect("/")


##############################################################################
# General user routes:

# TODO: HostMessaging  UserProfile  UserLikes


###############################################################################
# Listing routes:

# TODO: homepage  individualListings

@app.get('/')
def all_listings():
    """returns JSON for all available properties
    [{id, title, description, price, image[], user_id, rating}]"""

    listings = Listing.query.all()
    serialized = [l.serialize() for l in listings]

    return jsonify(listings=serialized)


@app.get('/listing/<int:id>')
def single_listing(id):
    """returns detailed info on single listing as JSON
    {id, title, description, price, image[], user_id, rating} """

    listing = Listing.query.get_or_404(id)
    serialized = listing.serialize()

    return jsonify(listing=serialized)



@app.post('/listing')
def create_listing():
    """Create new listing for property"""

    received = json.loads(request.form.get('data'))
    files = request.files['files']
    image_url = ''
    # form = ListingAddForm(csrf_enabled=False, data=received)


    if True: #FIXME: validate data being received
        title = received["title"]
        description = received["description"]
        location = received["location"]
        price = received["price"]
        user_id = received["user_id"]
        rating = received["rating"]

        try:
            image_url = upload_file(files)
        except ClientError as e:
            #TODO: default image
            print(e)

        listing = Listing(
            title=title,
            description=description,
            location=location,
            price=price,
            image_url=image_url,
            user_id=user_id,
            rating=rating
        )


        print(listing)
        db.session.add(listing)
        db.session.commit()

        serialized = listing.serialize()

        return jsonify(listing=serialized)

    #return jsonify(errors=form.errors) FIXME:



# @app.patch('/listing/<int:id>')
# def edit_listing():
#     """update listing"""


# @app.delete('/listing/<int:id>')
# def delete_listing():
    """Delete listing from database"""
