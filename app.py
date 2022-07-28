import os
from dotenv import load_dotenv

from flask import Flask, jsonify, render_template, request, flash, redirect, json
from flask_debugtoolbar import DebugToolbarExtension

from forms import ListingAddForm, UserAddForm, LoginForm
from models import db, connect_db, User, Listing
from aws import upload_file

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


# @app.before_request
# def add_csrf_to_g():
#     """add CSRFProtection Form to Flask global"""

#     g.csrf_form = CSRFProtectForm()

# api won't track login status
# def do_login(user):
#     """Log in user."""

#     session[CURR_USER_KEY] = user.id

# api won't track login status
# def do_logout():
#     """Log out user."""

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]


# @app.route('/signup', methods=["GET", "POST"])
# def signup():
#     """Handle user signup.

#     Create new user and add to DB. Redirect to home page.

#     If form not valid, present form.

#     If the there already is a user with that username: flash message
#     and re-present form.
#     """

#     # if CURR_USER_KEY in session:
#     #     del session[CURR_USER_KEY]
#     form = UserAddForm()

#     if form.validate_on_submit():
#         try:
#             user = User.signup(
#                 username=form.username.data,
#                 password=form.password.data,
#                 email=form.email.data,
#                 first_name=form.first_name.data,
#                 last_name=form.last_name.data,
#                 bio=form.bio.data,
#                 is_host=form.is_host.data

#                 # image_url=form.image_url.data or User.image_url.default.arg,
#             )
#             db.session.commit()

#         # except IntegrityError:
#         #     flash("Username already taken", 'danger')
#         #     return render_template('users/signup.html', form=form)


#         # return redirect("/")

#     else:
#         return render_template('users/signup.html', form=form)

# @app.route('/register', methods=['GET', 'POST'])
# def signup_user():
#  data = request.get_json()

#  hashed_password = generate_password_hash(data['password'], method='sha256')

#  new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
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


# TODO: update image storage
@app.post('/listing')
def create_listing():
    """Create new listing for property"""
    print("post listing")

    print('request', request)
    print('request.form', request.form['data'])
    received = json.loads(request.form.get('data'))
    files = request.files['files']
    image_url = ''
    form = ListingAddForm(csrf_enabled=False, data=received)
    print("data=", received)
    print("title=", received["title"])
    print('form.data=', form.data)
    print('files=', files)
    print('files.name=', files.filename)

    if True:
        print("form valid")
        title = received["title"]
        description = received["description"]
        location = received["location"]
        price = received["price"]

        if(upload_file(files.filename)):
            image_url = upload_file(files)
            #TODO: default image

        listing = Listing(
            title=title,
            description=description,
            location=location,
            price=price,
            image_url=image_url
        )


        print(listing)
        db.session.add(listing)

        serialized = listing.serialize()

        return jsonify(listing=serialized)

    return jsonify(errors=form.errors)



# @app.patch('/listing/<int:id>')
# def edit_listing():
#     """update listing"""


# @app.delete('/listing/<int:id>')
# def delete_listing():
    """Delete listing from database"""
