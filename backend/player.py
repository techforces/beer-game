"""Handle instructor querries."""
import json
from flask import Blueprint, abort, request
from flask_expects_json import expects_json
from middleware import player_registered
from src.connection import connector
from src.constants import Game_Role
from src.game import Game

bp = Blueprint('/player', __name__, url_prefix='/player')

schemas = {
    'join': {
        'type': 'object',
        'properties': {
            'game_id': {'type': 'number'},
            'game_role': {
                'type': 'string',
                'pattern': '^(factory|distributor|retailer|wholesaler)$'
            },
        },
        'required': ['game_id', 'game_role']
    },
    'play': {
        'type': 'object',
        'properties': {
            'purchase_units': {'type': 'number'},
        }
    }
}


@bp.route('join', methods=['POST'])
@expects_json(schemas['join'])
@player_registered
def join_game(player_id):
    """Join a game."""
    data = request.json
    # check if the position is empty
    player_role = Game_Role[data['game_role'].upper()]
    is_empty = connector.is_game_role_available(data['game_id'], player_role)
    if is_empty is not True:
        abort(400, f'Unable to add player to game: {is_empty}')
    # fill the position
    succ = connector.add_player_game(player_id, data['game_id'],
                                     player_role)
    if not succ:
        abort(400, 'Unable to add player to the game')
    return json.dumps({'success': True}), 200


@bp.route('game', methods=['GET'])
@player_registered
def get_game(player_id):
    """Get the player game."""
    game_id = connector.get_player_game_id(player_id)
    if not game_id:
        return json.dumps({'message': 'No game state found'})
    game = Game(connector, game_id)
    return json.dumps(game.get_state(player_id)), 200


@bp.route('game/play', methods=['POST'])
@expects_json(schemas['play'])
@player_registered
def play_game(player_id):
    """Play the player game."""
    game_id = connector.get_player_game_id(player_id)
    if not game_id:
        return json.dumps({'message': 'No game state found'})
    data = request.json
    game = Game(connector, game_id)
    succ = game.play(player_id, data['purchase_units'])
    return json.dumps({'success': succ}), 200
