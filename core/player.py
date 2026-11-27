from core.items import Item, Equipable, Consumable
from ui.display import Affichage
from ui.views import VueSelectionEquipe, VueSelectionCibleObjet, VueInventaire

#player
class Player:
  def __init__(self,name, score = 0, team = None, inventory = None):
    self.name = name
    self.score = score
    self.team = team if team is not None else []
    self.inventory = inventory if inventory is not None else []

  def __str__(self):
    team_str = ', '.join(str(member) for member in self.team)
    inventory_str = ', '.join(str(item) for item in self.inventory)
    return f"Player: {self.name}, Score: {self.score}, Team: [{team_str}], Inventory: [{inventory_str}]"

  def create_team(self, available_characters):
    while len(self.team) < 3:
      availables = [char for char in available_characters if char not in self.team]
      chosen = self.pick_character(availables)
      self.team.append(chosen)
    return self.team



  def pick_character(self, available_characters):
    while True:
      index = Affichage.display_vue(VueSelectionEquipe(self.team,available_characters), max_index=len(available_characters))
      if index is not None:
        return available_characters[index]

  def is_team_alive(self):
    return any(member.is_alive() for member in self.team) 

  def check_inventory(self):
    if not self.inventory:
      Affichage.display_vue(VueInventaire(self.inventory, self.team))
      return None

    item_index = Affichage.display_vue(VueInventaire(self.inventory, self.team), max_index=len(self.inventory))
    if item_index is None:
      return None

    item = self.inventory[item_index]
    target_index = Affichage.display_vue(VueSelectionCibleObjet(item, self.team), max_index=len(self.team))
    if target_index is None:
      return None

    target = self.team[target_index]
    self.use_item(item, target)
    return f"{item.name} utilisé(e) sur {target.name}."

  def use_item(self, item, target):
    if isinstance(item, Consumable):
      item.use(target)
      self.inventory.remove(item)
    elif isinstance(item, Equipable):
      if not target.is_slot_available(item.item_type):
        old_item = target.get_equipment(item.item_type)
        target.unequip_item(old_item)
        self.inventory.append(old_item)
      target.equip_item(item)
      self.inventory.remove(item)