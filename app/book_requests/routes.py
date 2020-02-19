from flask import jsonify, request
from app import db
from app.models import BookRequest, BookTitles
from app.book_requests import bp
from app.errors.errors import bad_request, not_found
from email_validator import validate_email, EmailNotValidError


@bp.route('/request', methods=['GET'])
def get_requests():
    data = BookRequest.to_collection_list(BookRequest.query)
    return jsonify(data)


@bp.route('/request', methods=['POST'])
def create_request():
    data = request.get_json() or {}

    if 'email' not in data or 'title' not in data:
        return bad_request('must include email and title fields')

    if data['title'] not in BookTitles.titles:
        return bad_request('Book not in library: {}'.format(BookTitles.titles))

    try:
        validate_email(data['email'], False, False, False)
    except EmailNotValidError as e:
        return bad_request('email validation failed: {}'.format(e))

    book_request = BookRequest()
    book_request.from_dict(data)

    db.session.add(book_request)
    db.session.commit()

    response = jsonify(book_request.to_dict())
    response.status_code = 201

    return response


@bp.route('/request/<int:id>', methods=['GET'])
def get_request(id):
    return jsonify(BookRequest.query.get_or_404(id).to_dict())


@bp.route('/request/<int:id>', methods=['DELETE'])
def delete_request(id):
    query = BookRequest.query.filter_by(id=id)
    if query.count() > 0:
        query.delete()
        db.session.commit()
        response = jsonify()
        response.status_code = 200
        return response
    else:
        return not_found("{}".format(id))


