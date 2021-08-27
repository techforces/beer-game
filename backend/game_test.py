"""Perform unit test for DB Operations."""
import unittest
from src.connection import Connector
from src.constants import Role, Game_Role
from src.game import Game
from yoyo import read_migrations
from yoyo import get_backend
import os

test_db = os.getenv('TEST_SQLITE_DB')
migrations = read_migrations('db_migrations')


class GameLogicTests(unittest.TestCase):
    def setUp(self):
        # Discard the database if exists 
        if os.path.exists(test_db):
            os.remove(test_db)
        backend = get_backend('sqlite:///{}'.format(test_db))
        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))
        self.conn = Connector(True, test_db)

    def test_factory_play_game_start(self):
        # Setup the game state by creating game 
        # users and assigning them roles in the 
        # game
        ins_id = self.conn.add_user('ins@test.test', 'asdaqe2sqwswsqw12esdqw', Role.INSTRUCTOR)
        self.assertEqual(ins_id, 1)

        factory_pl = self.conn.add_user('factory_pl@test.test', 'asdaqe2sqwswsqw12esdqw', Role.PLAYER)
        self.assertEqual(factory_pl, 2)

        distributor_pl = self.conn.add_user('distributor_pl@test.test', 'asdaqe2sqwswsqw12esdqw', Role.PLAYER)
        self.assertEqual(distributor_pl, 3)

        retailer_pl = self.conn.add_user('retailer_pl@test.test', 'asdaqe2sqwswsqw12esdqw', Role.PLAYER)
        self.assertEqual(retailer_pl, 4)

        wholesaler_pl = self.conn.add_user('wholesaler_pl@test.test', 'asdaqe2sqwswsqw12esdqw', Role.PLAYER)
        self.assertEqual(wholesaler_pl, 5)

        game_id = self.conn.create_game(ins_id)
        self.assertIsNotNone(game_id)
        game = Game(self.conn, game_id)

        succ = self.conn.add_player_game(wholesaler_pl, game_id, Game_Role.WHOLESALER)
        self.assertTrue(succ)

        succ = self.conn.add_player_game(retailer_pl, game_id, Game_Role.RETAILER)
        self.assertTrue(succ)

        succ = self.conn.add_player_game(distributor_pl, game_id, Game_Role.DISTRIBUTOR)
        self.assertTrue(succ)

        succ = self.conn.add_player_game(factory_pl, game_id, Game_Role.FACTORY)
        self.assertTrue(succ)

        # Check if players can play
        # Only the factory whould be allowed to play in the start
        (can_play, week) = game.can_play(factory_pl, Game_Role.FACTORY)
        self.assertTrue(can_play)
        self.assertEqual(week, 1)

        (can_play, _) = game.can_play(wholesaler_pl, Game_Role.WHOLESALER)
        self.assertFalse(can_play)

        (can_play, _) = game.can_play(distributor_pl, Game_Role.DISTRIBUTOR)
        self.assertFalse(can_play)

        (can_play, _) = game.can_play(retailer_pl, Game_Role.RETAILER)
        self.assertFalse(can_play)

        # Now play for the factory
        play_succ = game.play(factory_pl, 10)
        self.assertTrue(play_succ)

        # Everyone should not be able to play the game 
        # other than the distributor
        (can_play, _) = game.can_play(factory_pl, Game_Role.FACTORY)
        self.assertFalse(can_play)

        (can_play, week) = game.can_play(distributor_pl, Game_Role.DISTRIBUTOR)
        self.assertTrue(can_play)
        self.assertEqual(week, 1)

        (can_play, _) = game.can_play(wholesaler_pl, Game_Role.WHOLESALER)
        self.assertFalse(can_play)

        (can_play, _) = game.can_play(retailer_pl, Game_Role.RETAILER)
        self.assertFalse(can_play)

        #If I play with Retailer now it should not succeed
        play_succ = game.play(retailer_pl, 10)
        self.assertFalse(play_succ)

        # I should be able to play with distibutor, wholesaler and then retailer
        play_succ = game.play(distributor_pl, 10)
        self.assertTrue(play_succ)

        play_succ = game.play(wholesaler_pl, 10)
        self.assertTrue(play_succ)

        play_succ = game.play(retailer_pl, 10)
        self.assertTrue(play_succ)

        # Now I should be able to play with factory again but for week 2
        (can_play, week) = game.can_play(factory_pl, Game_Role.FACTORY)
        self.assertTrue(can_play)
        self.assertEqual(week, 2)


if __name__ == '__main__':
    unittest.main()