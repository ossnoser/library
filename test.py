import unittest
import os
from app import create_test_app, db
from flask_testing import TestCase


class ConfigTest:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


class MyTest(TestCase):

    def create_app(self):
        app = create_test_app(ConfigTest)
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_response_400(self):
        response = self.client.post("/request", json=dict(email='wrong', title='wrong'))
        assert 400 == response.status_code

    def test_response_404(self):
        response = self.client.get("/wrong_endpoint")
        assert 404 == response.status_code

    def test_create_read_request(self):
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

    def test_create_request_error(self):
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

    def test_read_error(self):
        response = self.client.get("/request/9999")
        assert 404 == response.status_code

    def test_delete_error(self):
        response = self.client.delete("/request/9999")
        assert 404 == response.status_code

    def test_delete_request(self):
        response = self.client.post("/request", json=dict(email='a@b.com', title='Deep Learning with Python'))
        id = response.json['id']
        response = self.client.delete("/request/{}".format(id))
        assert 200 == response.status_code


if __name__ == '__main__':
    unittest.main()

