from application import client, db, app
# from app import app
import json
from application.forms import LoginForm
from flask import render_template, flash, redirect, Response, request, url_for
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
from application.resources.ProfileRecourse import Profile, OAuth, ProfileSchema
from application.resources.BrandResource import Brand, BrandSchema
from flask_dance.contrib.google import google
from application import oauth

app.register_blueprint(oauth.google_blueprint, url_prefix="/login")

# @app.route('/')
# @app.route('/index')
# def index():
#     if current_user.is_authenticated:
#         user = {"username": current_user.username}
#     else:
#         user = {"username": "Please login"}
#     return render_template('index.html', title='Home', user=user)


# @app.route('/google', methods=['GET', 'POST'])
# def login_google():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#
#     if not google.authorized:
#         return redirect(url_for("google.login"))
#
# @app.route('/profile', methods=["GET"])
# def profile():
#     return render_template('profile.html', user=current_user)


## Use form to login
# form = LoginForm()
# if form.validate_on_submit():
#     user = ProfileRecourse.query.filter_by(username=form.username.data).first()
#     if user is None or not user.check_password(form.password.data):
#         flash('Invalid username or password')
#         return redirect(url_for('login'))
#     login_user(user, remember=form.remember_me.data)
#     return redirect(url_for('index'))
# return render_template('login.html', title='Sign In', form=form)


# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     flash("You have logged out")
#     return redirect(url_for("index"))


# @app.route('/register', methods=['POST'])
# def register():
#     info = json.loads(request.data)
#     try:
#         # If the user is already login in
#         if current_user.is_authenticated:
#             rsp = Response("You have already logged in!", status=200, content_type='text/plain')
#             return rsp
#
#         user_info = Profile.parse_info(info)
#         # Check if username exists
#         """TO-DO: check colloquial_name name as well"""
#         is_valid = Profile.validate_existence(user_info)
#         if not is_valid:
#             rsp = Response("Please use a different username", status=400, content_type='text/plain')
#             return rsp
#
#         # Find this OAuth token in the database, or create it
#         oauth = OAuth.validate_existence(OAuth.parse_info(info))
#         user = Profile(**user_info)
#         # Associate the new local user account with the OAuth token
#         oauth.user = user
#         # Save and commit to our database models
#         db.session.add_all([user, oauth])
#         db.session.commit()
#         # Log in the new local user account
#         login_user(user)
#         rsp = Response('New user has been registered', status=200, content_type='text/plain')
#         return rsp
#     except Exception as exp:
#         app.logger.error('Exception in register(): {}'.format(exp))
#         rsp = Response("Internal error", status=500, content_type='text/plain')
#         return rsp


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     try:
#         profile_schema = ProfileSchema()
#         if current_user.is_authenticated:
#             rsp = Response("User already logged in.", status=200, content_type='text/plain')
#             return rsp
#
#         info = json.loads(request.data)
#         email = Profile.parse_info(info)["email"]
#         # Retrieve user info with email
#         user = Profile.query.filter_by(email=email).first()
#         if user:
#             rsp = Response(json.dumps(profile_schema.dump(user)), status=200, content_type="application/json")
#             o = OAuth.validate_existence(info)
#             o.token = info["token"]
#             if not o.user:
#                 o.user = user
#             db.session.add_all([o, user])
#             db.session.commit()
#             login_user(user)
#         else:
#             rsp = Response("User associated with this email does not exist yet. Please register first", status=404,
#                            content_type='text/plain')
#
#         return rsp
#
#     except Exception as exp:
#         app.logger.error('Exception in profile(): {}'.format(exp))
#         rsp = Response("Internal error", status=500, content_type='text/plain')
#         return rsp

# @app.route('/brands/<id>', methods=['GET'])
# def brands(id):
#
#     try:
#         brand_schema = BrandSchema()
#         brand = Brand.query.filter_by(id=id).first()
#
#         if brand is None:
#             rsp = Response("Brand does not exist in the database", status=404, content_type='text/plain')
#         else:
#
#             brand = json.dumps(brand_schema.dump(brand), default=str)
#             rsp = Response(brand, status=200, content_type="application/json")
#         return rsp
#     except Exception as exp:
#         app.logger.error('Exception in brands(id): {}'.format(exp))
#         rsp = Response("Internal error", status=500, content_type='text/plain')
#         return rsp


@app.route('/users/<id>', methods=['GET', 'PUT', 'POST'])
def users(id):
    try:
        profile_schema = ProfileSchema()
        if request.method == 'GET':
            # if not current_user.is_authenticated():
            #     rsp = Response("Please first login.", status=403, content_type='text/plain')
            #     return rsp
            user = Profile.query.filter_by(id=id).first()
            if user is None:
                rsp = Response("User does not exist.", status=404, content_type='text/plain')
            else:

                user_json = json.dumps(profile_schema.dump(user), default=str)
                rsp = Response(user_json, status=200, content_type="application/json")

        # Update profile
        elif request.method == 'PUT':
            info = json.loads(request.data)
            new_user = Profile.update(id, info)
            db.session.add(new_user)
            db.session.commit()
            rsp = Response("User info update success.", status=200, content_type='text/plain')

        elif request.method == 'POST':
            info = json.loads(request.data)
            new_user = Profile(**Profile.parse_info(info))
            db.session.add(new_user)
            db.session.commit()
            rsp = Response("New user added success.", status=200, content_type='text/plain')

        return rsp

    except Exception as exp:
        app.logger.error('Exception in users(id): {}'.format(exp))
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp
