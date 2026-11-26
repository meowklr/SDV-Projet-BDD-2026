from core.items import Item, Equipable, Consumable

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
    print("\nChoisissez un personnage :")
    for i, char in enumerate(available_characters, start=1):
      print(f"{i}. {char.name} (HP: {char.hp}, ATK: {char.attack}, DEF: {char.defense})")
    while True:
      choice = input("Numéro du personnage : ").strip()
      if choice.isdigit() and 1 <= int(choice) <= len(available_characters):
        return available_characters[int(choice) - 1]
      print("Choix invalide, réessayez.")

  def is_team_alive(self):
    return any(member.is_alive() for member in self.team) 

  def check_inventory(self):
    if not self.inventory:
      print("Inventaire vide.")
      return None
    print("\nInventaire :")
    for i, item in enumerate(self.inventory, start=1):
      print(f"{i}. {item.name} ({item.item_type} - {item.rarity})")
    while True:
      choice = input("Numéro de l'objet (0 pour annuler) : ").strip()
      if choice == "0":
        return None
      if choice.isdigit() and 1 <= int(choice) <= len(self.inventory):
        return self.inventory[int(choice) - 1]
      print("Choix invalide, réessayez.")

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