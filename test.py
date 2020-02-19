import unittest
import os
from app import create_app, db
from flask_testing import TestCase


class ConfigTest:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'non-indovinerai-mai'
    JWT_SECRET_KEY = SECRET_KEY
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    TESTING = True


class BookRequestTest(TestCase):

    def create_app(self):
        app = create_app(ConfigTest)
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_response_404(self):
        response = self.client.get("/wrong_endpoint")
        assert 404 == response.status_code

    def test_create_and_read(self):
        response = self.client.post("/request", json=dict(email='a@b.com', title='Deep Learning with Python'))
        assert 201 == response.status_code
        assert 'email' in response.json.keys()
        assert 'id' in response.json.keys()
        assert 'title' in response.json.keys()
        assert 'timestamp' in response.json.keys()

        created = response.json
        response = self.client.get("/request/{}".format(created['id']))

        for key in created.keys():
            assert created[key] == response.json[key]

    def test_create_with_error(self):
        response = self.client.post("/request", json=dict(email='mail@wrong,com'))
        assert 400 == response.status_code
        response = self.client.post("/request", json=dict(title='Deep Learning with Python'))
        assert 400 == response.status_code
        response = self.client.post("/request", json=dict(email='mail@wrong,com', title='Deep Learning with Python'))
        assert 400 == response.status_code
        response = self.client.post("/request", json=dict(email='mail@right.com', title='Deep Learning with Java'))
        assert 400 == response.status_code

    def test_read_requests(self):
        for i in range(4):
            response = self.client.post("/request", json=dict(email='a@b.com', title='Deep Learning with Python'))
            assert 201 == response.status_code
        response = self.client.get("/request")
        assert len(response.json) == 4

    def test_read_with_error(self):
        response = self.client.get("/request/9999")
        assert 404 == response.status_code

    def test_delete_with_error(self):
        response = self.client.delete("/request/9999")
        assert 404 == response.status_code

    def test_delete(self):
        response = self.client.post("/request", json=dict(email='a@b.com', title='Deep Learning with Python'))
        id = response.json['id']
        response = self.client.delete("/request/{}".format(id))
        assert 200 == response.status_code


class UserTest(TestCase):

    def create_app(self):
        app = create_app(ConfigTest)
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_user_and_get_token(self):
        response = self.client.post("/user", json=dict(
            email='a@b.com', name='Mario', surname='Rossi', password='chi-lo-sa?'))
        assert 201 == response.status_code
        id = response.json['id']
        response = self.client.post("/user/login", json=dict(email='a@b.com', password='chi-lo-sa?'))
        assert 200 == response.status_code
        access_token = response.json.get('access_token', None)
        assert access_token is not None
        return access_token, id

    def test_create_authenticate_and_read(self):
        response = self.client.post("/user", json=dict(
            email='a@b.com', name='Mario', surname='Rossi', password='chi-lo-sa?'))
        assert 201 == response.status_code
        assert 'email' in response.json.keys()
        assert 'id' in response.json.keys()
        assert 'name' in response.json.keys()
        assert 'surname' in response.json.keys()

        created = response.json

        response = self.client.post("/user/login", json=dict(email='a@b.com', password='chi-lo-sa?'))
        assert 200 == response.status_code
        access_token = response.json.get('access_token', None)
        assert access_token is not None

        response = self.client.get("/user/{}".format(created['id']), headers=dict(
            Authorization="Bearer {}".format(access_token)))

        for key in created.keys():
            assert created[key] == response.json[key]

    def test_create_with_error(self):
        response = self.client.post("/user", json=dict(email='something@is.missing.com'))
        assert 400 == response.status_code
        response = self.client.post("/user", json=dict(name='something is missing'))
        assert 400 == response.status_code
        response = self.client.post("/user", json=dict(email='mail@wrong,com', name='Mario', surname='Rossi'))
        assert 400 == response.status_code

    def test_read_users(self):
        for i in range(4):
            response = self.client.post("/user", json=dict(
                email='user{}@b.com'.format(i),
                password='password{}'.format(i),
                name='Mario{}'.format(i),
                surname='Rossi'.format(i)))
            assert 201 == response.status_code
        response = self.client.post("/user/login", json=dict(email='user0@b.com', password='password0'))
        assert 200 == response.status_code
        access_token = response.json.get('access_token', None)
        assert access_token is not None
        response = self.client.get("/user", headers=dict(
            Authorization="Bearer {}".format(access_token)))
        assert len(response.json) == 4

    def test_read_with_error(self):
        access_token, id = self.create_user_and_get_token()
        response = self.client.get("/user/9999", headers=dict(
            Authorization="Bearer {}".format(access_token)))
        assert 404 == response.status_code

    def test_delete_with_error(self):
        access_token, id = self.create_user_and_get_token()
        response = self.client.delete("/user/9999", headers=dict(
            Authorization="Bearer {}".format(access_token)))
        assert 404 == response.status_code

    def test_delete(self):
        access_token, id = self.create_user_and_get_token()
        response = self.client.delete("/user/{}".format(id), headers=dict(
            Authorization="Bearer {}".format(access_token)))
        assert 200 == response.status_code


if __name__ == '__main__':
    unittest.main()

