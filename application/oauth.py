from application import db
from application.config import Config
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized, oauth_error
from application.resources.ProfileRecourse import OAuth, Profile
from sqlalchemy.orm.exc import NoResultFound
from flask_login import current_user, login_user
from flask import flash

google_blueprint = make_google_blueprint(
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    scope=['https://www.googleapis.com/auth/userinfo.email',
           'https://www.googleapis.com/auth/userinfo.profile'],
    offline=True,
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,
    )
)

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Google.", category="error")
        return False

    resp = blueprint.session.get("/oauth2/v1/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return False
    info = resp.json()
    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=info["id"])
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=info["id"], token=token)

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with Google.")

    else:
        # Create a new local user account for this user
        user_info = {"email": info["email"],
                     "username": info["given_name"] + info["family_name"] + info["id"][3:10],
                     "colloquial_name": info["given_name"] + info["family_name"] + info["id"][3:10],
                     "waist": "2",
                     "height": "3",
                     "bust": "4",
                     "shoulder_width": "2",
                     'brand_id': "kk",
                     'style_id': "kas"}
        user = Profile(**user_info)
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in with Google.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False


# notify on OAuth provider error
@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, message, response):
    msg = "OAuth error from {name}! " "message={message} response={response}".format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")
