"""Create a helper class to manage game querries."""
from .constants import Game_Role

# Helper variable to check the sequence of players
game_role_sequence = {
    Game_Role.PRODUCTION: 0,
    Game_Role.FACTORY: 1,
    Game_Role.DISTRIBUTOR: 2,
    Game_Role.WHOLESALER: 3,
    Game_Role.RETAILER: 4,
    Game_Role.CUSTOMER: 5
}

game_role_sequence_r = {
    0: Game_Role.PRODUCTION,
    1: Game_Role.FACTORY,
    2: Game_Role.DISTRIBUTOR,
    3: Game_Role.WHOLESALER,
    4: Game_Role.RETAILER,
    5: Game_Role.CUSTOMER,
}


class Game():
    """Manage a game instance."""

    def __init__(self, connector, game_id):
        """Init a game instance.

        Args:
            game_id (init): game id
        """
        self.game_id = game_id
        self.connector = connector
        self.game = self.connector.get_game(self.game_id)

    def get_role_supplier(self, player_role):
        """Get the supplier of the player role.

        Args:
            player_role (Game_Role): role of the player
            to find supplier role for

        Returns:
            Game_Role: role of the supplier of the player role
        """
        return game_role_sequence_r[game_role_sequence[player_role] - 1]

    def get_role_customer(self, player_role):
        """Get the customer of the player role.

        Args:
            player_role (Game_Role): role of the player
            to find customer role for

        Returns:
            Game_Role: role of the customer of the player role
        """
        return game_role_sequence_r[game_role_sequence[player_role] + 1]

    def get_state(self, player_id):
        """Get the game state based on the player_id.

        Args:
            player_id (int): id of player
        """
        player_role = self.connector.get_player_role(player_id, self.game_id)
        if not player_role:
            return False
        (can_play, week) = self.can_play(player_id, player_role)

        dummy_game_state = {
            'week': week,
            'backorder': 3,
            'incoming_orders': 3,
            'total_requirement': 6,
            'inventory': 5,
            'shipment': 6,
            'total_inventory': 11,
            'unit_shipped': 3,
            'ending_inventory': 8,
            'holding_cost': 10,
            'backlog_cost': 5,
            'role': player_role.value,
            'supplier': self.get_role_supplier(player_role).value,
            'customer': self.get_role_customer(player_role).value,
            'can_play': can_play
        }

        return {'game': self.game, 'game_state': dummy_game_state}

    def can_play(self, player_id, player_role):
        """Check if the role can play for a certain week.

        Args:
            player_role (Game_Role): role to check

        Returns:
            (bool, week): if the player can play, if so which week.
        """
        # get the already played week
        week_played = self.connector.get_player_last_week(
            player_id,
            self.game_id
        )

        player_pos = game_role_sequence[player_role]

        # TODO: handle the case where the wholesaler/ retailer is not present
        # TODO: check if the game is over if the week_played == game_week
        # if it is not week 0 and it is the first player of the round
        # check if last player has played
        if week_played != 0 and player_pos == 1:
            has_played = self.connector.has_role_played_week(
                self.game_id,
                game_role_sequence_r[4],
                week_played
            )
            if not has_played:
                return (False, week_played)
        # If it is not the first player then just check the last
        # player played in the same week.
        elif player_pos != 1:
            has_played = self.connector.has_role_played_week(
                self.game_id,
                game_role_sequence_r[player_pos - 1],
                week_played + 1
            )
            if not has_played:
                return (False, week_played)
        return (True, week_played + 1)

    def play(self, player_id, order_units):
        """Create an order in the game for the player.

        Args:
            player_id (int): player id for whom the order has to placed
            order_units (int): units of orders

        Returns:
            boolean: bool telling if the order placement was successful
        """
        # get the player game role
        player_role = self.connector.get_player_role(player_id, self.game_id)
        if not player_role:
            return False

        # Check if the player can play in the next week.
        (can_play, week) = self.can_play(player_id, player_role)
        if not can_play:
            return False
        # add players order request for the current week
        return self.connector.add_player_game_state(
            self.game_id,
            player_id,
            week,
            order_units
        )
