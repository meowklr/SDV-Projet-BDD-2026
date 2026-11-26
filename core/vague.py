import random
from core.entities import Entity, Character, Enemy
from db.db_init import DifficultyList

#vague
class Vague:
  def __init__(self, current_vague, enemies):
    self.current_vague = current_vague
    self.enemies = enemies

  def pick_enemies(self, current_vague):
    # Logic to pick enemies based on the current wave
    self.enemies = range(int(current_vague * self.get_difficulty()))

  def play_vague(self, player):
    while player.is_team_alive() and any(enemy.is_alive() for enemy in self.enemies):
      self._play_team_turns(player)
      self._play_enemy_turns(player)

  def _play_team_turns(self, player):
    for member in player.team:
      if not member.is_alive():
        continue

      enemy = next((enemy for enemy in self.enemies if enemy.is_alive()), None)
      if enemy is None:
        break

      member.play_turn(enemy)
      if not enemy.is_alive():
        player.inventory.extend(enemy.drop_loot())

  def _play_enemy_turns(self, player):
    living_members = [member for member in player.team if member.is_alive()]
    for enemy in self.enemies:
      if not enemy.is_alive() or not living_members:
        continue
      enemy.play_turn(random.choice(living_members))
      living_members = [member for member in player.team if member.is_alive()]

  def get_difficulty(self):
    # Logic to determine the difficulty of the wave based on the wave number
      for difficulty in DifficultyList:
        if difficulty.lap == self.current_vague:
          return difficulty
      return None