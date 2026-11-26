import random

class Entity:
  def __init__(self, name, hp, max_hp, attack, defense):
    self.name = name
    self.hp = hp
    self.max_hp = max_hp
    self._attack = attack
    self._defense = defense

  @property
  def attack(self):
    return self._attack

  @property
  def defense(self):
    return self._defense


  def is_alive(self):
    return self.hp > 0

  def take_damage(self, damage):
    self.hp -= damage
    if self.hp < 0:
      self.hp = 0

  def heal(self, amount):
    self.hp += amount
    if self.hp > self.max_hp:
      self.hp = self.max_hp

  def attack_target(self, target):
    damage = max(1, self.attack - target.defense)
    target.take_damage(damage)
    return damage

  def play_turn(self, target):
    self.attack_target(target)


#character est la classe enfant de entity
class Character(Entity):
  def __init__(self, name, hp, max_hp, attack, defense, equipment = None):
    super().__init__(name, hp, max_hp, attack, defense)
    self.equipment = equipment if equipment is not None else []

  @property
  def attack(self):
    total_attack = self._attack
    for item in self.equipment:
      total_attack += item.stats.get("attack", 0)
    return total_attack

  @property
  def defense(self):
    total_defense = self._defense
    for item in self.equipment:
      total_defense += item.stats.get("defense", 0)
    return total_defense

  def equip_item(self, item):
    self.equipment.append(item)

  def unequip_item(self, item):
    if item in self.equipment:
      self.equipment.remove(item)

  def is_slot_available(self, slot_name : str):
    for item in self.equipment:
      if item.item_type == slot_name:
        return False
    return True

  def get_equipment(self, slot_name : str):
    for item in self.equipment:
      if item.item_type == slot_name:
        return item
    return None

  def project_damage(self, target):
    return max(1, self.attack - target.defense)

  def play_turn(self, target):
    #choix inventaire ou attaquer
    self.attack_target(target)

class Enemy(Entity):
  def __init__(self, name, hp, max_hp, attack, defense, loots = None):
    super().__init__(name, hp, max_hp, attack, defense)
    self.loots = loots if loots is not None else []

  def drop_loot(self):
    #tirer au sort les objets droppés selon leur droprate et leur rareté
    dropped_items = []
    for item in self.loots:
      if random.random() < item.droprate:
        dropped_items.append(item)
    return dropped_items
