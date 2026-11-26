from core.game import Game
from core.entities import Entity, Character, Enemy
from core.items import Item, Equipable, Consumable
from ui.display import Affichage
from db.models import CharacterDB
class View:
  def __init__(self):
    """Initialize the View class."""
    pass

  def inventory_view(self, list, team):
    # Logic to display the inventory view
    pass

  def player_turn_view(self, team, character, enemies):
    # Logic to display the player's turn view
    pass

  def target_selection_view(self, team, character, enemies):
    # Logic to display the target selection view
    pass

  def turn_info_view(self, team, event, enemies):
    # Logic to display the turn information view
    pass  

  def team_selection_view(self, team, list_selection):
    # Logic to display the team selection view
    pass

  def title_screen_view(self):
    # Logic to display the title screen view
    pass

  def leaderboard_view(self, scores):
    # Logic to display the leaderboard view
    pass

  def game_over_view(self):
    # Logic to display the game over view
    pass

  def load_game_view(self):
    # Logic to display the load game view
    pass

  def exit_view(self):
    # Logic to display the exit view
    pass
