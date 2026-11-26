from core.items import Item, Equipable, Consumable
from ui.display import Display

#player
class Player:
  def __init__(self,name, score = 0, team = None, inventory = None):
    self.name = name
    self.score = score
    self.team = team if team is not None else []
    self.inventory = inventory if inventory is not None else []

  def create_team(self, available_characters):
    while len(self.team) < 3:
      availables = [char for char in available_characters if char not in self.team]
      chosen = self.pick_character(availables)
      self.team.append(chosen)
    return self.team

  def pick_character(self, available_characters):
    character = Display.display_character_selection(available_characters)
    return character  

  def is_team_alive(self):
    return any(member.is_alive() for member in self.team) 

  def check_inventory(self):
    item = Display.display_inventory(self.inventory)
    return item  

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