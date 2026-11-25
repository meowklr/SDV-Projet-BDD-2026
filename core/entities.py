#entity, character, enemy
class Entity:
  def _init__(self, name, hp, max_hp, attack, defense):
    self.name = name
    self.hp = hp
    self.max_hp = max_hp
    self.attack = attack
    self.defense = defense

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

  def attack(self, target):
    damage = self.attack - target.defense
    if damage < 0:
      damage = 1
    target.take_damage(damage)
    return damage

  def play_turn(self, target):
    self.attack(target)


#character est la classe enfant de entity
class Character(Entity):
  def __init__(self, attaque, defense, equipment): #attack et defense sont des propriétés calculées overrides
    self.equipment = equipment
    _attack = attaque
    _defense = defense

  @property
  def attack(self):
    total_attack = self._attack
    for item in self.equipment:
      total_attack += item.attack
    return total_attack

  @property
  def defense(self):
    total_defense = self._defense
    for item in self.equipment:
      total_defense += item.defense
    return total_defense

  def equip_item(self, item):
    self.equipment.append(item)

  def unequip_item(self, item):
    if item in self.equipment:
      self.equipment.remove(item)

  def is_slot_available(self, slot_name = str):
    for item in self.equipment:
      if item.slot == slot_name:
        return False
    return True

  def get_equipment(self, slot_name = str):
    for item in self.equipment:
      if item.slot == slot_name:
        return item
    return None

  def project_damage(self, target):
    target_copy = target.copy()
    return self.attack(target_copy)

 """ def play_turn(self):"""
    #appeler l'affichage
    #recuperer le choix de l'action du joueur
    #executer l'action choisie

class Enemy(Entity):
  def __init__(self, loots):
    self.loots = loots

  def drop_loot(self):
    return self.loots

 """ def play_turn(self):"""
    #appeler l'affichage
    #recuperer le choix de l'action de l'ennemi
    #executer l'action choisie