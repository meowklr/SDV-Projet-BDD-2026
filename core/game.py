import os
import sys
import pymongo
from core.entities import Character, Enemy
from core.items import Equipable, Consumable
from core.vague import Vague
from core.player import Player

class Game:
  def __init__(self, player):
    self.player = player
    self.vague = Vague(current_vague=1, enemies=[])
    self.client = pymongo.MongoClient("mongodb://localhost:27017/")
    self.db = self.client["game_rayan_db"]

  def load_game(self):
    # Load the game state from a file or database
    pass

  def launch_game(self):
    while self.player.is_team_alive():
      self.vague.pick_enemies(self.vague.current_vague)
      self.vague.play_vague(self.player)
      if self.player.is_team_alive():
        self.vague.current_vague += 1
        self.player.score += 1
      else:
        self.db["scores"].insert_one({"player_name": self.player.name, "score": self.player.score})
        break

  def show_leaderboard(self):
    scores = self.db["scores"].find().sort("score", pymongo.DESCENDING)
    print("Leaderboard:")
    for score in scores:
      print(f"{score['player_name']}: {score['score']}")

  def exit(self):
      self.client.close()
      sys.exit(0)
