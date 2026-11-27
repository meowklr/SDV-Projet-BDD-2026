import os
import sys
import pymongo
from core.entities import Character
from core.vague import Vague
from db.db_init import CharacterList
from db.models import ScoreDB
from ui.display import Affichage
from ui.views import OPTIONS_GAME_OVER, VueGameOver, VueLeaderboard


class Game:
  def __init__(self, player):
    self.player = player
    self.vague = Vague(current_vague=1, enemies=[])
    self.client = pymongo.MongoClient(
      os.getenv("MONGO_URL", "mongodb://localhost:27017/")
    )
    self.db = self.client["game_rayan_db"]

  def load_characters(self):
    try:
      docs = list(self.db["characters"].find())
    except Exception:
      docs = []
    if not docs:
      docs = CharacterList
    return [
      Character(
        name=c["name"],
        hp=c["hp"],
        max_hp=c["hp"],
        attack=c["attack"],
        defense=c["defense"],
      )
      for c in docs
    ]

  def save_game(self):
    # Save the game state to a file or database
    pass

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
        self.db["scores"].insert_one({
          "player_name": self.player.name,
          "score": self.player.score,
        })
        choice = Affichage.display_vue(VueGameOver(), max_index=len(OPTIONS_GAME_OVER))
        if choice in (1, None):
          self.exit()
        break

  def show_leaderboard(self):
    docs = list(self.db["scores"].find().sort("score", pymongo.DESCENDING).limit(10))
    scores = [ScoreDB(player_name=doc["player_name"], score=doc["score"]) for doc in docs]
    Affichage.display_vue(VueLeaderboard(scores))

  def exit(self):
    self.client.close()
    sys.exit(0)
