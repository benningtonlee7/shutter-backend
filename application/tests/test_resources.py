from application import db
from application.resources import ProfileRecourse, BrandResource
import unittest
from random import randint
import os

os.environ.get('DATABASE_URL') or 'mysql+pymysql://{username}:' \
                                  '{password}@{host}/{db_name}'.format(username="root",
                                                                       password="dbuser666",
                                                                       host="localhost",
                                                                       db_name="shutter")


class TestResource(unittest.TestCase):

    def setUp(self):
        self.user = {"email": "abc{}@columbia.edu".format(randint(1, 100)),
                     "username": "csa{}".format(randint(1, 100)),
                     "colloquial_name": "qsdc{}".format(randint(1, 100)),
                     "waist": "2{}".format(randint(1, 100)),
                     "height": "3{}".format(randint(1, 100)),
                     "bust": "123{}".format(randint(1, 100)),
                     "shoulder_width": "123{}".format(randint(1, 100)),
                     'brand_id': "asd{}".format(randint(1, 100)),
                     'style_id': "asasd{}".format(randint(1, 100))}

    def test_user_create(self):
        profile = ProfileRecourse.Profile(**self.user)
        db.session.add(profile)
        db.session.commit()
        res = ProfileRecourse.Profile.query.all()
        self.assertIsNotNone(res)


    def test_user_delete(self):
        res = ProfileRecourse.Profile.query.all()
        for p in res:
            db.session.delete(p)
        db.session.commit()
        new_q = ProfileRecourse.Profile.query.all()
        self.assertEqual(0, len(new_q))


if __name__ == '__main__':
    unittest.main()
