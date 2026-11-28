import random
from core.entities import Enemy
from core.items import Consumable, Equipable
from db.db_init import DifficultyList, EnemyListDict, ItemListDict, RarityList, VagueList
from ui.display import Affichage
from ui.views import OPTIONS_TOUR, VueChoixCible, VueInfoTour, VueTourJoueur

RARITY_RATES = {r["name"]: r["drop_rate"] for r in RarityList}

class Vague:
  def __init__(self, current_vague, enemies):
    self.current_vague = current_vague
    self.enemies = enemies

  def __str__(self):
    enemies_str = ', '.join(str(enemy) for enemy in self.enemies)
    return f"Vague: {self.current_vague}, Enemies: [{enemies_str}]"

  def _build_loot_items(self, dropable_items, item_multiplier = 1.0):
    loots = []
    for item_db in dropable_items:
      droprate = min(1.0, RARITY_RATES.get(item_db.rarity, 0.1) * item_multiplier)
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
      loots = self._build_loot_items(tpl.dropable, diff["item_multiplier"])
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

      living_enemies = [enemy for enemy in self.enemies if enemy.is_alive()]
      if not living_enemies:
        break

      while True:
        action = Affichage.display_vue(
          VueTourJoueur(player.team, member, living_enemies),
          max_index=len(OPTIONS_TOUR),
        )
        if action is None:
          continue

        if action == 0:
          target_index = Affichage.display_vue(
            VueChoixCible(player.team, member, living_enemies),
            max_index=len(living_enemies),
          )
          if target_index is None:
            continue

          target = living_enemies[target_index]
          damages = member.attack_target(target)
          event = f"{member.name} attaque {target.name} et inflige {damages} dégâts."

          if not target.is_alive():
            loots = target.drop_loot()
            player.inventory.extend(loots)
            event += f"\n{target.name} est vaincu !"
            if loots:
              event += "\nLoot : " + ", ".join(item.name for item in loots)

          Affichage.display_vue(VueInfoTour(player.team, event, self.enemies))
          break

        elif action == 1:
          event = player.check_inventory()
          if event is None:
            continue
          Affichage.display_vue(VueInfoTour(player.team, event, self.enemies))
          break

        elif action == 2:
          event = f"{member.name} passe son tour."
          Affichage.display_vue(VueInfoTour(player.team, event, self.enemies))
          break


  def _play_enemy_turns(self, player):
    for enemy in self.enemies:
      living_members = [member for member in player.team if member.is_alive()]
      if not enemy.is_alive() or not living_members:
        continue
      target = random.choice(living_members)
      damages = enemy.attack_target(target)
      event = f"{enemy.name} attaque {target.name} et inflige {damages} dégâts."
      Affichage.display_vue(VueInfoTour(player.team, event, self.enemies))

  def get_difficulty(self):
    lap = (self.current_vague - 1) // 10 + 1
    for difficulty in DifficultyList:
      if difficulty["lap"] == lap:
        return difficulty
    return DifficultyList[-1]
