"""Class to manage the DB Operations."""
import os.path
import secrets
import os
import datetime
from dotenv import load_dotenv
import sqlite3
import mariadb
import logging
from .constants import Role, Game_Role

load_dotenv()

is_sqlite = os.getenv("SQLITE")
is_sqlite = is_sqlite.lower() in ['true', '1', 'y', None, '']
sqlite_file = os.getenv("SQLITE_DB")


class Connector:
    """Manage Databse connection."""

    def __init__(self, is_testing=False, test_sqlite=None):
        """Init Databse connection."""
        if is_testing:
            self.conn = sqlite3.connect(
                test_sqlite, check_same_thread=False
            )
        elif is_sqlite is True:
            self.conn = sqlite3.connect(
                sqlite_file, check_same_thread=False)
        else:
            try:
                self.conn = mariadb.connect(
                    user=os.getenv("MARIADB_USERNAME"),
                    password=os.getenv("MARIADB_PASSWORD"),
                    host=os.getenv("MARIADB_HOST"),
                    port=int(os.getenv("MARIADB_PORT", 3306)),
                    database=os.getenv("MARIADB_DATABASE")
                )
            except mariadb.Error as e:
                logging.error('Error_Connector: {}'.format(e))

    def __to_dict(self, cursor, values):
        """Turn a tuple of values into a dictictonary.

        Args:
            cursor: database connection cursor, use right after required query
            values(tuple): a SINGLE TUPLE filled with desired values
        Returns:
            d(dict): a dictionary of key-value pairs
        """
        d = {}
        if not values:
            return None
        for i, v in zip(cursor.description, values):
            d[i[0]] = v
        return d

    def add_user(self, email, password_hash, role):
        """Add User to user table.

        Args:
            email (string): emailaddress of the user
            password_hash (string): password
        """
        cur = self.conn.cursor()
        try:
            cur.execute(
                'INSERT INTO User(email, password_hash, role) VALUES (?, ?, ?)',
                (email, password_hash, role.value)
            )
            self.conn.commit()
            cur.execute(
                'SELECT id FROM User WHERE email = ?',
                (email,)
            )
            _id = cur.fetchall()[0][0]
            return _id
        except (sqlite3.Error, mariadb.Error) as e:
            logging.error('Error_Connector_add_user: {}'.format(e))
            return None
        finally:
            cur.close()

    def get_user(self, email, password_hash):
        """Get All Users."""
        cur = self.conn.cursor()
        try:
            cur.execute(
                'SELECT id, role FROM User WHERE email = ? AND password_hash = ?',
                (email, password_hash,)
            )
            res = cur.fetchall()
            if len(res) < 1:
                return None
            return {
                'id': res[0][0],
                'role': res[0][1]
            }
        except (sqlite3.Error, mariadb.Error) as e:
            logging.error(
                'Error_Connector_get_users: {}'.format(e)
            )
            return None
        finally:
            cur.close()

    def add_user_session(self, user_id):
        """Add session for user authentication.

        Args:
            user_id (int): the id of the user
        Returns:
            session_id (string): session id
        """
        cur = self.conn.cursor()
        try:
            token = secrets.token_urlsafe()
            cur.execute(
                'INSERT INTO UserSession (token, user_id) VALUES (?, ?)',
                (token, user_id)
            )
            self.conn.commit()
        except (sqlite3.Error, mariadb.Error) as e:
            logging.error('Error_Connector_add_user_session: {}'.format(e))
            return None
        finally:
            cur.close()
        return token

    def check_session_validity(self, token, role=None):
        """Check the session validity.

        Args:
            token (string): session token
            ROLE (Role): optional role to specify for instructor/player
        Returns:
            user_id (int): the user id associated with the session,
            None if session id is expired or invalid
        """
        cur = self.conn.cursor()
        try:
            if role not in [None, Role.PLAYER, Role.INSTRUCTOR]:
                raise TypeError("expected None, Role.Player, Role.instructor in ROLE")
            date_30_min_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
            if role:
                cur.execute(
                    "SELECT s.user_id FROM UserSession s \
                    INNER JOIN User u on u.role = ? AND u.id = s.user_id WHERE token = ? AND\
                    s.creation_time >= ? ",
                    (role.value, token, date_30_min_ago)
                )
            else:
                cur.execute(
                    "SELECT user_id FROM UserSession WHERE token = ? AND\
                    creation_time >= ?",
                    (token, date_30_min_ago)
                )
            res = cur.fetchall()
            if len(res) < 1:
                return None

            cur.execute(
                "UPDATE UserSession SET creation_time=CURRENT_TIMESTAMP WHERE token = ?",
                (token,)
            )
            self.conn.commit()
            return res[0][0]
        except (sqlite3.Error, mariadb.Error) as e:
            print(e)
            logging.error(
                'Error_Connector_check_session_validity: {}'.format(e)
            )
            return None
        finally:
            cur.close()

    def get_users(self):
        """Get All Users."""
        cur = self.conn.cursor()
        try:
            cur.execute(
                'SELECT id, email FROM user'
            )
            res = cur.fetchall()
            return res
        except (sqlite3.Error, mariadb.Error) as e:
            logging.error(
                'Error_Connector_get_users: {}'.format(e)
            )
            return None
        finally:
            cur.close()
        # maintaining clarity
    def create_game(self, instructor_id, session_length=26, active=True, wholesaler_present=True,
     retailer_present=True, demand_pattern_id=None, info_delay=2, info_sharing=False,
     holding_cost=0.5, backlog_cost=1, starting_inventory=5 ) -> int:
        """Creates a game

        Args:
            instructor_id(int): instructor id
            session_length(int): length of game session, default 26
            active(bool): whether the game is active, default True
            wholesaler_present(bool): whether wholesaler is present. Default True
            retailer present(bool): whether retailer is present. Default True
            demand_pattern_id(int): what demand pattern to use TODO IMPLEMENT (WIP)
            info_delay(int): how long it takes for orders to reach successor / predecessor. Default 2
            info_sharing(bool): whther info sharing between players is enabled. Default False
            holding_cost(float): holding cost for players. Default 0.5
            backlog_cost(float): cost for backlogged beer. Default 1
        Returns:
            Game_id(int): the id of the game created
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                'INSERT INTO Game ( instructor_id, session_length, retailer_present, wholesaler_present, \
                    holding_cost, backlog_cost, active, demand_pattern_id, \
                starting_inventory, info_delay, info_sharing ) VALUES \
                ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (
                    instructor_id, session_length, retailer_present,
                    wholesaler_present, holding_cost, backlog_cost,
                    active, demand_pattern_id, starting_inventory,
                    info_delay, info_sharing
                )
            )
            id_ = cur.lastrowid
            self.conn.commit()
            return id_
        except (sqlite3.Error, mariadb.Error) as e:
            logging.error('Error_Connector_create_game: {}'.format(e))
            return None
        finally:
            cur.close()

    def get_game(self, game_id):
        """Get a game's description.

        Args:
            game_id(int): the id of the game querried
        Returns:
            d(dict): A dictionary of key-value pairs corresponding to
                     column-value, None if error
        """
        try:
            cur = self.conn.cursor()
            cur.execute("select * from game where id = ?", (game_id,))
            d = self.__to_dict(cur, cur.fetchone())
            return d
        except (sqlite3.Error, mariadb.Error) as e:
            logging.error('Error_Connector_get_game: {}'.format(e))
            return None
        finally:
            cur.close()

    def get_games(self, instructor_id):
        """Get the list of all the games by the instructor.

        Args:
            instructor_id(int): the id of the game querried
        Returns:
            d(dict): list of games
        """
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT session_length, retailer_present, wholesaler_present,\
                         holding_cost, backlog_cost, instructor_id, active,\
                         demand_pattern_id, starting_inventory, info_delay,\
                         info_sharing, factory_id, distributor_id,\
                         retailer_id, wholesaler_id, id\
                         from game where instructor_id = ?',
                        (instructor_id,))
            res = cur.fetchall()
            games = []
            for g in res:
                game = {
                    "session_length": g[0],
                    "retailer_present": g[1],
                    "wholesaler_present": g[2],
                    "holding_cost": g[3],
                    "backlog_cost": g[4],
                    "instructor_id": g[5],
                    "active": g[6],
                    "demand_pattern_id": g[7],
                    "starting_inventory": g[8],
                    "info_delay": g[9],
                    "info_sharing": g[10],
                    "factory_id": g[11],
                    "distributor_id": g[12],
                    "retailer_id": g[13],
                    "wholesaler_id": g[14],
                    "id": g[15]
                }
                games.append(game)
            return games
        except (sqlite3.Error, mariadb.Error) as e:
            logging.error('Error_Connector_get_games: {}'.format(e))
            return None
        finally:
            cur.close()

    def is_game_role_available(self, game_id, game_role):
        """Check the availibility of a game role in a game.

        Args:
            game_id(int): id of the game to check
            game_role(Game_Role): game role to check
        Returns:
            success(bool): whether the player was added to the game
        """
        try:
            cur = self.conn.cursor()
            # check if the game is available
            cur.execute(
                f'SELECT 1 from game where id=?',
                (game_id,)
            )
            r = cur.fetchone()
            if r is None:
                return 'Invalid game id'
            # check if the game role is allowed
            if game_role in [Game_Role.RETAILER, Game_Role.WHOLESALER]:
                cur.execute(
                    f'SELECT {game_role.value}_present from game where id=?',
                    (game_id,)
                )
                r = cur.fetchone()
                if r[0] == 0:
                    return 'Disabled game role'

            # check if the game role is available
            cur.execute(
                f'SELECT {game_role.value}_id from game where id=?',
                (game_id,)
            )
            r = cur.fetchone()
            if r[0]:
                return 'Game role already occupied'
            return True
        except (sqlite3.Error, mariadb.Error) as e:
            logging.error(
                'Error_Connector_is_game_role_available: {}'.format(e)
            )
            return False
        finally:
            cur.close()

    def add_player_game(self, player_id, game_id, game_role):
        """Add a player to a game.

        Args:
            user_id(int): id of the user to be added to game
            game_id(int): id of the game to add the user to
            game_role(Game_Role): type of player
        Returns:
            success(bool): whether the player was added to the game
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                'INSERT into Player (id, current_game_id, role) values (?, ?, ?)',
                (player_id, game_id, game_role.value)
            )
            cur.execute(
                f'UPDATE game SET {game_role.value}_id = ? WHERE id = ?',
                (player_id, game_id)
            )
            self.conn.commit()
            return True
        except (sqlite3.Error, mariadb.Error) as e:
            logging.error('Error_Connector_add_player_game: {}'.format(e))
            return False
        finally:
            cur.close()

    def get_player_game_id(self, player_id):
        """Get the game played by the user.

        Args:
            user_id(int): id of the player
        Returns:
            game(game_id | None): game id if there is any game player by user
            or none
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                'SELECT current_game_id FROM Player WHERE id = ?',
                (player_id,)
            )
            r = cur.fetchone()
            if r is None:
                return False
            return r[0]
        except (sqlite3.Error, mariadb.Error) as e:
            logging.error('Error_Connector_get_player_game_id: {}'.format(e))
            return False
        finally:
            cur.close()

    def get_player_last_week(self, player_id, game_id):
        """Get the lasy played week for the player.

        Args:
            player_id (int): id of the player to fetch for
            game_id (int): id of the game to fetch for
        Returns:
            week(int): last played week cnt, 0 if start of the game
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                'SELECT MAX(week) FROM GameState WHERE\
                student_id = ? AND game_id = ?',
                (player_id, game_id)
            )
            r = cur.fetchone()
            if r[0] is None:
                return 0
            return r[0]
        except (sqlite3.Error, mariadb.Error) as e:
            logging.error('Error_Connector_get_player_last_week: {}'.format(e))
            return False
        finally:
            cur.close()

    def get_player_role(self, player_id, game_id):
        """Get player game role.

        Args:
            player_id (int): id of the player to fetch the role for
            game_id (int): game id of the player

        Returns:
            role: role of the player in the game
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                'SELECT role FROM Player WHERE\
                id = ? AND current_game_id = ?',
                (player_id, game_id)
            )
            r = cur.fetchone()
            if r is None:
                return False
            return Game_Role[r[0].upper()]
        except (sqlite3.Error, mariadb.Error) as e:
            logging.error('Error_Connector_get_player_role: {}'.format(e))
            return False
        finally:
            cur.close()

    def has_role_played_week(self, game_id, role, week):
        """Get player game role.

        Args:
            game_id (int): game id to check
            role (Game_Role): game role to check for
            week(int): week cnt to check for

        Returns:
            bool: if the role has played
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                'SELECT 1 FROM GameState as GS, Player as P WHERE\
                GS.game_id = ? AND GS.week = ? AND GS.student_id\
                = P.id AND P.role = ?',
                (game_id, week, role.value)
            )
            r = cur.fetchone()
            if r is None:
                return False
            return True
        except (sqlite3.Error, mariadb.Error) as e:
            logging.error('Error_Connector_get_player_role: {}'.format(e))
            return False
        finally:
            cur.close()

    def add_player_game_state(self, game_id, player_id, week, order_amount):
        """Add player game state.

        Args:
            game_id (int): game id
            player_id (int): player id
            week (int): week cnt
            order_amount (int): order amount

        Returns:
            bool: success
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                'INSERT into GameState(game_id, student_id, week, order_amount)\
                values (?, ?, ?, ?)',
                (game_id, player_id, week, order_amount)
            )
            return True
        except (sqlite3.Error, mariadb.Error) as e:
            logging.error('Error_Connector_get_player_role: {}'.format(e))
            return False
        finally:
            cur.close()


connector = Connector()
