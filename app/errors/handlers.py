from app.errors.errors import error_response
from app.errors import bp


@bp.app_errorhandler(401)
def internal_error(error):
    return error_response(401)


@bp.app_errorhandler(404)
def not_found_error(error):
    return error_response(404)


@bp.app_errorhandler(405)
def not_found_error(error):
    return error_response(405)


@bp.app_errorhandler(500)
def internal_error(error):
    return error_response(500)
