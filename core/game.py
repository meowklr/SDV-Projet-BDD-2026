import os
import sys
import pymongo
from core.entities import Character
from core.player import Player
from core.vague import Vague
from db.db_init import CharacterList
from db.models import CharacterSaveDB, MonsterSaveDB, SaveDB, ScoreDB
from ui.display import Affichage
from ui.views import OPTIONS_GAME_OVER, VueChargerSauvegarde, VueGameOver, VueLeaderboard


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
    game_state = {
      "player_name": self.player.name,
      "score": self.player.score,
      "current_vague": self.vague.current_vague,
      "equipe": [
        {
          "name": member.name,
          "hp": member.hp,
          "max_hp": member.max_hp,
          "attack": member._attack,
          "defense": member._defense,
          "equipement": [item.name for item in member.equipment],
        }
        for member in self.player.team
      ],
      "monsters": [
        {"name": enemy.name, "hp": enemy.hp}
        for enemy in self.vague.enemies
        if enemy.is_alive()
      ],
      "inventaire": [item.name for item in self.player.inventory],
    }
    self.db["saves"].replace_one(
      {"player_name": self.player.name},
      game_state,
      upsert=True,
    )

  def load_game(self):
    docs = list(self.db["saves"].find())
    if not docs:
      Affichage.display_vue(VueChargerSauvegarde([]))
      return False

    sauvegardes = [
      SaveDB(
        player_name=doc["player_name"],
        score=doc["score"],
        equipe=[
          CharacterSaveDB(name=character["name"], hp=character["hp"], equipement=[])
          for character in doc.get("equipe", doc.get("team", []))
        ],
        monsters=[
          MonsterSaveDB(name=monster["name"], hp=monster["hp"])
          for monster in doc.get("monsters", [])
        ],
        inventaire=[],
      )
      for doc in docs
    ]

    index = Affichage.display_vue(
      VueChargerSauvegarde(sauvegardes),
      max_index=len(sauvegardes),
    )
    if index is None:
      return False

    doc = docs[index]
    team_docs = doc.get("equipe", doc.get("team", []))
    team = [
      Character(
        name=member["name"],
        hp=member["hp"],
        max_hp=member.get("max_hp", member["hp"]),
        attack=member.get("attack", 15),
        defense=member.get("defense", 5),
      )
      for member in team_docs
    ]
    self.player = Player(name=doc["player_name"], score=doc["score"], team=team)
    self.vague = Vague(
      current_vague=doc.get("current_vague", doc["score"] + 1),
      enemies=[],
    )
    self.launch_game()
    return True

  def launch_game(self):
    while self.player.is_team_alive():
      self.vague.pick_enemies(self.vague.current_vague)
      self.vague.play_vague(self.player)
      if self.player.is_team_alive():
        self.vague.current_vague += 1
        self.player.score += 1
        self.save_game()
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
