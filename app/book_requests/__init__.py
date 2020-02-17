from flask import Blueprint

bp = Blueprint('book_requests', __name__)

from app.book_requests import routes
