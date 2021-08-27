"""Perform unit test for DB Operations."""
import unittest
from src.connection import Connector
from src.constants import Role, Game_Role
from yoyo import read_migrations
from yoyo import get_backend
import os

test_db = os.getenv('TEST_SQLITE_DB')
migrations = read_migrations('db_migrations')


class DatabaseOperationsTests(unittest.TestCase):
    def setUp(self):
        # Discard the database if exists 
        if os.path.exists(test_db):
            os.remove(test_db)
        backend = get_backend('sqlite:///{}'.format(test_db))
        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))
        self.conn = Connector(True, test_db)

    def test_user_signup(self):
        res = self.conn.add_user('test@test.test', 'asdaqe2sqwswsqw12esdqw', Role.INSTRUCTOR)
        self.assertEqual(res, 1)
        data = self.conn.get_users()
        emails = [row[1] for row in data]
        self.assertTrue('test@test.test' in emails)

    def test_valid_user_session(self):
        # Add a test user
        user_id = self.conn.add_user('test@test.test', 'asdaqe2sqwswsqw12esdqw', Role.INSTRUCTOR)
        self.assertEqual(user_id, 1)

        # Create a user session
        token = self.conn.add_user_session(user_id)

        # check the session validity
        session_user_id = self.conn.check_session_validity(token)
        self.assertEqual(session_user_id, user_id)

    def test_expired_user_session(self):
        # Add a test user
        user_id = self.conn.add_user('test@test.test', 'asdaqe2sqwswsqw12esdqw', Role.INSTRUCTOR)
        self.assertEqual(user_id, 1)

        # Add a 35 min old timestamp
        token = 'random_string'
        cur = self.conn.conn.cursor()
        cur.execute(
            "INSERT INTO UserSession (token, user_id, creation_time) VALUES (?, ?, datetime('now', '-35 minutes'))",
            (token, user_id)
        )
        cur.close()

        # verify that there is no session
        session_user_id = self.conn.check_session_validity(token)
        self.assertEqual(session_user_id, None)

    def test_game_creation(self):
        #create game by instructor w/ id 1
        g = self.conn.create_game(1)
        self.assertTrue(g is not None,msg="game creation returnedNone")

    def test_game_info(self):
        #create game
        g = self.conn.create_game(1)
        self.assertTrue(g is not None, msg="none returned for game creation")
        #use created game id
        d = self.conn.get_game(g)
        self.assertTrue(d is not None, msg="game info not properly returned")

    def test_game_creation_custom_params(self):
        d = {
            'session_length': 22,
            'active': False,
            'wholesaler_present': False,
            'retailer_present': True,
            'demand_pattern_id': 2,
            'info_delay': 3,
            'info_sharing': False,
            'holding_cost': 6.9,
            'backlog_cost': 4.20,
        }
        g = self.conn.create_game(1, **d)
        self.assertTrue(g is not None, msg="game instance returned None")
        dict_query = self.conn.get_game(g)
        for i in d:
            self.assertEqual(d[i], dict_query[i], msg=f'error, key {i} differs: {d[i]}, {dict_query[i]}')

    def test_list_instructor_games(self):
        # # Add a test user
        ins_id = self.conn.add_user('test@test.test', 'asdaqe2sqwswsqw12esdqw', Role.INSTRUCTOR)
        self.assertEqual(ins_id, 1)
        
        #create games
        game1 = self.conn.create_game(ins_id)
        self.assertIsNotNone(game1)

        game2 = self.conn.create_game(ins_id)
        self.assertIsNotNone(game2)
        
        all_games = self.conn.get_games(ins_id)
        self.assertEqual(len(all_games), 2)
        self.assertEqual(all_games[0]['id'], game1)
        self.assertEqual(all_games[1]['id'], game2)

    def test_is_role_available_case0(self):
        # In case0 we test the base case that on the start
        # of the game all the roles should be available
        ins_id = self.conn.add_user('ins@test.test', 'asdaqe2sqwswsqw12esdqw', Role.INSTRUCTOR)
        self.assertEqual(ins_id, 1)
        
        game1 = self.conn.create_game(ins_id)
        self.assertIsNotNone(game1)

        is_available = self.conn.is_game_role_available(game1, Game_Role.WHOLESALER)
        self.assertTrue(is_available)

        is_available = self.conn.is_game_role_available(game1, Game_Role.DISTRIBUTOR)
        self.assertTrue(is_available)

        is_available = self.conn.is_game_role_available(game1, Game_Role.FACTORY)
        self.assertTrue(is_available)

        is_available = self.conn.is_game_role_available(game1, Game_Role.RETAILER)
        self.assertTrue(is_available)


    def test_is_role_available_case1(self):
        # In case1 we test the case where wholesaler and 
        # retailer are disabled. At the start of the game 
        # all the roles should be available other than
        # the disabled ones
        ins_id = self.conn.add_user('ins@test.test', 'asdaqe2sqwswsqw12esdqw', Role.INSTRUCTOR)
        self.assertEqual(ins_id, 1)
        
        game1 = self.conn.create_game(ins_id, wholesaler_present=False, retailer_present=False)
        self.assertIsNotNone(game1)

        is_available = self.conn.is_game_role_available(game1, Game_Role.WHOLESALER)
        self.assertEqual(is_available, 'Disabled game role')

        is_available = self.conn.is_game_role_available(game1, Game_Role.DISTRIBUTOR)
        self.assertTrue(is_available)

        is_available = self.conn.is_game_role_available(game1, Game_Role.FACTORY)
        self.assertTrue(is_available)

        is_available = self.conn.is_game_role_available(game1, Game_Role.RETAILER)
        self.assertEqual(is_available, 'Disabled game role')

    def test_is_role_available_case2(self):
        # In case2 we test the case where the game is 
        # not present.
        # All the roles should be not available

        game_id = 5
        is_available = self.conn.is_game_role_available(game_id, Game_Role.WHOLESALER)
        self.assertEqual(is_available, 'Invalid game id')

        is_available = self.conn.is_game_role_available(game_id, Game_Role.DISTRIBUTOR)
        self.assertEqual(is_available, 'Invalid game id')

        is_available = self.conn.is_game_role_available(game_id, Game_Role.FACTORY)
        self.assertEqual(is_available, 'Invalid game id')

        is_available = self.conn.is_game_role_available(game_id, Game_Role.RETAILER)
        self.assertEqual(is_available, 'Invalid game id')

    def test_add_player(self):
        ins_id = self.conn.add_user('ins@test.test', 'asdaqe2sqwswsqw12esdqw', Role.INSTRUCTOR)
        self.assertEqual(ins_id, 1)

        player_id = self.conn.add_user('pl@test.test', 'asdaqe2sqwswsqw12esdqw', Role.PLAYER)
        self.assertEqual(player_id, 2)
        
        game1 = self.conn.create_game(ins_id)
        self.assertIsNotNone(game1)

        is_available = self.conn.is_game_role_available(game1, Game_Role.WHOLESALER)
        self.assertTrue(is_available)

        succ = self.conn.add_player_game(player_id, game1, Game_Role.WHOLESALER)

        # only the wholesaler should be disabled
        is_available = self.conn.is_game_role_available(game1, Game_Role.WHOLESALER)
        self.assertEqual(is_available, 'Game role already occupied')

        is_available = self.conn.is_game_role_available(game1, Game_Role.DISTRIBUTOR)
        self.assertTrue(is_available)

        is_available = self.conn.is_game_role_available(game1, Game_Role.FACTORY)
        self.assertTrue(is_available)

        is_available = self.conn.is_game_role_available(game1, Game_Role.RETAILER)
        self.assertTrue(is_available)

    def test_player_game_id(self):
        ins_id = self.conn.add_user('ins@test.test', 'asdaqe2sqwswsqw12esdqw', Role.INSTRUCTOR)
        self.assertEqual(ins_id, 1)

        player_id = self.conn.add_user('pl@test.test', 'asdaqe2sqwswsqw12esdqw', Role.PLAYER)
        self.assertEqual(player_id, 2)

        game1 = self.conn.create_game(ins_id)
        self.assertIsNotNone(game1)

        is_available = self.conn.is_game_role_available(game1, Game_Role.WHOLESALER)
        self.assertTrue(is_available)

        succ = self.conn.add_player_game(player_id, game1, Game_Role.WHOLESALER)
        self.assertTrue(succ)

        player_game = self.conn.get_player_game_id(player_id)
        self.assertEqual(player_game, game1)



if __name__ == '__main__':
    unittest.main()