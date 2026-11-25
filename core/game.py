#game
from core.vague import Vague
from core.player import Player

class Game:
  def __init__(self, player):
    self.player = player

  def load_game(self):
    # Load the game state from a file or database
    pass

  def launch_game(self):
    while self.player.is_alive():
      print(f"Début de la vague {wave.number} !")
      wave.play_vague(self.player)
      if not self.player.is_alive():
        print("Game Over!")
        return
    print("Congratulations! You have completed all waves.")
