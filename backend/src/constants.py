"""Constants and Configurations."""
from enum import Enum

class Role(Enum):
    """Enum class for User Roles."""

    PLAYER = 'player'
    INSTRUCTOR = 'instructor'

class Game_Role(Enum):
    """Enum class for game player roles"""
    PRODUCTION = 'production'
    FACTORY = 'factory'
    DISTRIBUTOR = 'distributor'
    WHOLESALER = 'wholesaler'
    RETAILER = 'retailer'
    CUSTOMER = 'customer'
