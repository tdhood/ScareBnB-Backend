import os
from dotenv import load_dotenv

from flask import Flask, jsonify, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import ListingAddForm, UserAddForm, LoginForm, MessageForm, CSRFProtectForm, UserEditForm
from models import db, connect_db, User, Listing, LikedMessage, DEFAULT_HEADER_IMAGE_URL, DEFAULT_IMAGE_URL

load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

connect_db(app)

#############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.before_request
def add_csrf_to_g():
    """add CSRFProtection Form to Flask global"""

    g.csrf_form = CSRFProtectForm()


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Log out user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                # image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


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
    """Displays available properties"""

    listings = Listing.query.all()

    return jsonify(listings)


@app.get('/listing/<int:id>')
def single_listing(id):
    """Displays detailed info on single listing"""

    listing = Listing.query.get_or_404(id)

    return jsonify(listing)


# TODO: update image storage
@app.post('/listing')
def create_listing():
    """Create new listing for property"""

    received = request.json

    form = ListingAddForm(csrf_enabled=False, data=received)

    if form.validate_on_submit():
        title = received["title"]
        description = received["description"]
        location = received["location"]
        price = received["price"]
        image_url = received["image_url"]

        listing = Listing(
            title=title,
            description=description,
            location=location,
            price=price,
            image_url=image_url
        )

        db.session.add(listing)


@app.patch('/listing/<int:id>')
def edit_listing():
    """update listing"""


@app.delete('/listing/<int:id>')
def delete_listing():
    """Delete listing from database"""
