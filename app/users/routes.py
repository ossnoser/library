from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token
from app import db
from app.models import User
from app.book_requests import bp
from app.errors.errors import bad_request, not_found, unauthorized
from email_validator import validate_email, EmailNotValidError


@bp.route('/user', methods=['GET'])
@jwt_required
def get_users():
    data = User.to_collection_list(User.query)
    return jsonify(data)


@bp.route('/user/<int:id>', methods=['GET'])
@jwt_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/user', methods=['POST'])
def create_user():
    email = request.json.get('email')
    password = request.json.get('password')
    name = request.json.get('name')
    surname = request.json.get('surname')
    if email is None or password is None or name is None or surname is None:
        return bad_request('must include email, password, name and surname fields')
    try:
        validate_email(email, False, False, False)
    except EmailNotValidError as e:
        return bad_request('email validation failed: {}'.format(e))
    if User.query.filter_by(email=email).first() is not None:
        return bad_request('{} already exist'.format(email))
    user = User(email=email, name=name, surname=surname)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@bp.route('/user/<int:id>', methods=['DELETE'])
@jwt_required
def delete_user(id):
    query = User.query.filter_by(id=id)
    if query.count() > 0:
        query.delete()
        db.session.commit()
        response = jsonify()
        response.status_code = 200
        return response
    else:
        return not_found("{}".format(id))


@bp.route('/user/login', methods=['POST'])
def user_login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if email is None or password is None:
        return bad_request('must include email and password')

    user = User.query.filter_by(email=email).first()
    if user is None:
        return bad_request('{} is not registered'.format(email))

    if user.verify_password(password):
        return jsonify({'access_token': create_access_token(identity=email)}), 200

    return unauthorized("Bad email or password")
