from rich.console import Console
from rich.panel import Panel
from InquirerPy import inquirer
from core.game import Game
from core.entities import Entity, Character, Enemy
from core.items import Item, Equipable, Consumable
from ui.display import Affichage
from db.models import CharacterDB

class Display:
  def __init__(self):
    self.console = Console()
    self.console.clear()

  def display_view(self, function):
    self.clear()
    self.console.renderable()

  def show_error(self, error_message):
    print(f"Error: {error_message}")

  def create_info_box(self, title, info, box_color, text_color):
   #  logic to create an info box with the given parameters
    pass

  def create_select_box(self, title, items, index, box_color, text_color, hover_color):
    #logic to create a select box with the given parameters
    pass