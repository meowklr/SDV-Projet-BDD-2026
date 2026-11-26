import random
from core.entities import Enemy
from core.items import Consumable, Equipable
from db.db_init import DifficultyList, EnemyList, RarityList, VagueList

RARITY_RATES = {r["name"]: r["drop_rate"] for r in RarityList}

class Vague:
  def __init__(self, current_vague, enemies):
    self.current_vague = current_vague
    self.enemies = enemies

  def _build_loot_items(self, dropable_items):
    loots = []
    for item_db in dropable_items:
      droprate = RARITY_RATES.get(item_db.rarity, 0.1)
      item_cls = Consumable if item_db.consumable else Equipable
      loots.append(item_cls(
        name=item_db.name,
        description=item_db.name,
        droprate=droprate,
        rarity=item_db.rarity,
        item_type=item_db.item_type,
        stats=item_db.effect,
      ))
    return loots

  def pick_enemies(self, current_vague):
    self.current_vague = current_vague
    diff = self.get_difficulty()

    #trouve les monstres prévus pour cette vague (sinon tous les monstres)
    pool_names = None
    for vague_cfg in VagueList:
      if vague_cfg["start_number"] <= current_vague <= vague_cfg["end_number"]:
        pool_names = {m["name"] for m in vague_cfg["monsters"]}
        break

    pool = [m for m in EnemyList if pool_names is None or m.name in pool_names]
    nb_enemies = min(1 + (current_vague - 1) // 3, 3)

    self.enemies = []
    for _ in range(nb_enemies):
      tpl = random.choice(pool)
      hp = max(1, int(tpl.hp * diff["health_multiplier"]))
      atk = max(1, int(tpl.attack * diff["attack_multiplier"]))
      defense = max(0, int(tpl.defense * diff["defense_multiplier"]))
      loots = self._build_loot_items(tpl.dropable)
      self.enemies.append(Enemy(tpl.name, hp, hp, atk, defense, loots))
    return self.enemies

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
    for difficulty in DifficultyList:
      if difficulty["lap"] == self.current_vague // 10:
        return difficulty
    return DifficultyList[-1]
