"""REST Server."""
from flask import Flask, request, abort
from flask_cors import CORS
from flask_expects_json import expects_json
from src.connection import connector
from src.constants import Role
import json
import instructor
import player

app = Flask(__name__)

app.register_blueprint(instructor.bp)
app.register_blueprint(player.bp)
CORS(app)

# TODO: add the length for the password hash
schemas = {
    'authenticate': {
        'type': 'object',
        'properties': {
            'email': {
                'type': 'string',
                'format': 'email'
            },
            'passwordHash': {
                'type': 'string',
            }
        },
        'required': ['email', 'passwordHash']
    },
    'register': {
        'type': 'object',
        'properties': {
            'email': {
                'type': 'string',
                'format': 'idn-email'
            },
            'role': {
                'type': 'string',
                'pattern': '^(instructor|player)$'
            },
            'passwordHash': {
                'type': 'string',
            }
        },
        'required': ['email', 'role', 'passwordHash']
    }
}


@app.route('/authenticate', methods=['POST'])
@expects_json(schemas['authenticate'])
def authentication(name=None):
    """Verify player with name."""
    data = request.json
    user = connector.get_user(data['email'], data['passwordHash'])
    if not user:
        abort(400, 'Invalid user email or password.')
    token = connector.add_user_session(user['id'])
    if not token:
        abort(400, 'Something went wrong while authentication.')
    return json.dumps(
        {'SESSION-KEY': token, 'id': user['id'], 'role': user['role']}
    ), 200


@app.route('/register', methods=['POST'])
@expects_json(schemas['register'])
def register_user():
    """Register User."""
    data = request.json
    role = Role[data['role'].upper()]
    user_id = connector.add_user(data['email'], data['passwordHash'], role)
    if not user_id:
        abort(400, 'Something went wrong while registration.')
    token = connector.add_user_session(user_id)
    return json.dumps(
        {
            'success': True,
            'SESSION-KEY': token,
            'id': user_id,
            'role': role.value
        }
    ), 200


@app.route('/')
def welcome():
    """Welcome."""
    return 'Welcome!'

if __name__ == '__main__':
    app.run(port=8086, host='0.0.0.0')
