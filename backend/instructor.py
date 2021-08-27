"""Handle instructor querries."""
import json
from flask import Blueprint, abort, request
from flask_expects_json import expects_json
from middleware import instructor_registered
from src.connection import connector

bp = Blueprint('/instructor', __name__, url_prefix='/instructor')

schemas = {
    'game': {
        'type': 'object',
        'properties': {
            'session_length': {'type': 'number'},
            'active': {'type': 'boolean'},
            'wholesaler_present': {'type': 'boolean'},
            'retailer_present': {'type': 'boolean'},
            'demand_pattern_id': {' type': 'number'},
            'info_delay': {'type': 'number'},
            'info_sharing': {'type': 'boolean'},
            'holding_cost': {'type': 'number'},
            'backlog_cost': {'type': 'number'},
        },
        'required': []
    }
}


@bp.route('game', methods=['POST'])
@expects_json(schemas['game'])
@instructor_registered
def create_game(ins_id):
    """Create a game."""
    data = request.json
    # create game with
    g_id = connector.create_game(
        ins_id,
        **{i: data[i] for i in data if(i in schemas['game']['properties'])})
    if not g_id:
        abort(400, 'an unexpected error occurred')
    return json.dumps({"game_id": g_id})


@bp.route('games', methods=['GET'])
@instructor_registered
def list_game(ins_id):
    """Create a game."""
    # list all the game from the instructor
    games = connector.get_games(ins_id)
    return json.dumps({"games": games})


@bp.route('game/<id>', methods=['GET'])
@instructor_registered
def get_game(ins_id, id):
    """
    Get the information of a game instance.

    For now any instructor can access any game
    """
    return json.dumps(connector.get_game(id))
