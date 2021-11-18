from application import db, app
from flask import Flask, request
from application.resources import ProfileRecourse, BrandResource
from random import randint
import pytest
import json


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with app.test_client() as client:
        profile1 = ProfileRecourse.Profile(email="abc@gmail.com", username="abc", colloquial_name="abc",
                                          waist="1",height="2", bust="3", shoulder_width="4", brand_id ="brand_id",
                                          style_id="style_id")
        db.session.add(profile1)
        db.session.commit()
        yield client



def test_get_profile(client):
    url = 'http://127.0.0.1:5000/profile/19'
    rsp_get = client.get(url)
    data = json.loads(rsp_get.data)
    assert rsp_get.status_code == 200
    assert data["id"] == 19


def test_register_success(client):
    url = 'http://127.0.0.1:5000/register'
    info = {"email": "abc{}@columbia.edu".format(randint(1, 100)),
            "username": "csa{}".format(randint(1, 100)),
            "colloquial_name": "qsdc{}".format(randint(1, 100)),
            "waist": "2{}".format(randint(1, 100)),
            "height": "3{}".format(randint(1, 100)),
            "bust": "123{}".format(randint(1, 100)),
            "shoulder_width": "123{}".format(randint(1, 100)),
            'brand_id': "asd{}".format(randint(1, 100)),
            'style_id': "asasd{}".format(randint(1, 100)),
            'provider': "google",
            'provider_user_id': "116171818207986314604{}".format(randint(1, 200)),
            'token': {"scope": "abc{}".format(randint(1, 100))}}

    rsp_put = client.post(url, data=json.dumps(info, indent=4))
    assert rsp_put.status_code == 200
    assert rsp_put.data.decode("utf-8") == 'New user has been registered'


def test_register_invalid_username(client):
    url = 'http://127.0.0.1:5000/register'
    info = {"email": "abc{}@columbia.edu".format(randint(1, 100)),
            "username": "BenningtonLi1718182",
            "colloquial_name": "qsdc{}".format(randint(1, 100)),
            "waist": "2{}".format(randint(1, 100)),
            "height": "3{}".format(randint(1, 100)),
            "bust": "123{}".format(randint(1, 100)),
            "shoulder_width": "123{}".format(randint(1, 100)),
            'brand_id': "asd{}".format(randint(1, 100)),
            'style_id': "asasd{}".format(randint(1, 100)),
            'provider': "google",
            'provider_user_id': "116171818207986314604{}".format(randint(1, 200)),
            'token': {"scope": "abc{}".format(randint(1, 100))}}

    rsp_put = client.post(url, data=json.dumps(info, indent=4))
    assert rsp_put.status_code == 400
    assert rsp_put.data.decode("utf-8") == 'Please use a different username'
