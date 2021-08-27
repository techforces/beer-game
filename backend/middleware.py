"""Middleware to manage connection authentication."""
from functools import wraps
from flask import request, abort
from src.constants import Role
from src.connection import connector

# base function, not decorated
def user_registered(role=None):
    """Verify that the request is from a registered user."""
    token = request.headers.get('SESSION-KEY')
    if not token:
        abort(400, 'User not authenticated')
    res = connector.check_session_validity(token, role=role)
    if not res:
        abort(401, 'User SESSION-KEY is invalid or expired')
    return res

def instructor_registered(f):
    """Verify that the request is from a registered instructor
    Returns:
        ins_id(int): the id of the instructor,
                     to be used in a subsequent function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ins_id = user_registered(role=Role.INSTRUCTOR)
        return f(ins_id, *args, **kwargs)
    return decorated_function

def player_registered(f):
    """Verify that the request is from a registered player
    Returns:
        player_id(int): the id of the player, to
                        be used in a subsequent function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        player_id = user_registered(role=Role.PLAYER)
        return f(player_id, *args, **kwargs)
    return decorated_function
