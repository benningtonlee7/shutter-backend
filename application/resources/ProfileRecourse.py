from sqlalchemy import or_
from application import db, login, ma
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from sqlalchemy.orm.exc import NoResultFound


class Profile(UserMixin, db.Model):
    __tablename__ = 'Profile'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    waist = db.Column(db.String(10), index=True, unique=False, nullable=False)
    height = db.Column(db.String(10), index=True, unique=False, nullable=False)
    bust = db.Column(db.String(10), index=True, unique=False, nullable=False)
    shoulder_width = db.Column(db.String(10), index=True, unique=False, nullable=False)
    brand_id = db.Column(db.String(128), index=True, unique=False, nullable=False)
    style_id = db.Column(db.String(128), index=True, unique=False, nullable=False)

    def __repr__(self):
        return '<Profile user: {}, id: {}>'.format(self.username, self.id)

    @staticmethod
    def validate_existence(info):
        """TO-DO: might need to check if the info being passed in empty"""
        username, email = info["username"], info["email"]
        user = Profile.query.filter(or_(Profile.username == username, Profile.email == email)).first()
        if user is None:
            return True
        return False

    @classmethod
    def parse_info(cls, info):
        user_info = {"email": info["email"],
                     "username": info["username"],
                     "waist": info["waist"],
                     "height": info["height"],
                     "bust": info["bust"],
                     "shoulder_width": info["shoulder_width"],
                     'brand_id': info["brand_id"],
                     'style_id': info["style_id"]}

        return user_info

    @classmethod
    def update(cls, id, info):
        user_row = Profile.query.filter_by(id=id).first()
        user_row.username = info["username"]
        user_row.bust = info["bust"]
        user_row.height = info["height"]
        user_row.shoulder_width = info["shoulder_width"]
        user_row.waist = info["waist"]
        user_row.style_id = info["style_id"]
        user_row.brand_id = info["brand_id"]

        return user_row


class OAuth(OAuthConsumerMixin, db.Model):
    provider = db.Column(db.String(256), unique=False, nullable=False)
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Profile.id), nullable=False)
    user = db.relationship(Profile)

    @staticmethod
    def parse_info(info):
        oauth_info = {"provider": info["provider"],
                      "provider_user_id": info["provider_user_id"],
                      "token": info["token"]}

        return oauth_info

    @staticmethod
    def validate_existence(info):
        """TO-DO: might need to check if the info being passed in empty"""

        query = OAuth.query.filter_by(provider=info["provider"], provider_user_id=info["provider_user_id"])
        try:
            oauth = query.one()
        except NoResultFound:
            oauth = OAuth(provider=info["provider"], provider_user_id=info["provider_user_id"], token=info["token"])
        return oauth


class ProfileSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Profile

    id = ma.auto_field()
    email = ma.auto_field()
    username = ma.auto_field()
    waist = ma.auto_field()
    height = ma.auto_field()
    bust = ma.auto_field()
    shoulder_width = ma.auto_field()
    brand_id = ma.auto_field()
    style_id = ma.auto_field()


@login.user_loader
def load_profile(id):
    return Profile.query.get(int(id))
