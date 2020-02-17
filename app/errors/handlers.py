from app.book_requests.errors import error_response
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return error_response(404)


@bp.app_errorhandler(500)
def internal_error(error):
    return error_response(500)
