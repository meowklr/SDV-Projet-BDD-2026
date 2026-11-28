

class Item :
  def __init__(self, name, description, droprate, rarity, item_type, stats):
    self.name = name
    self.description = description
    self.droprate = droprate
    self.rarity = rarity
    self.item_type = item_type
    self.stats = stats

  def __str__(self):
    return f"{self.name} - {self.description} - Drop Rate: {self.droprate} - Rarity: {self.rarity} - Type: {self.item_type} - Stats: {self.stats}"

class Consumable(Item):
  def __init__(self, name, description, droprate, rarity, item_type, stats):
    super().__init__(name, description, droprate, rarity, item_type, stats)

  def use(self, target):
    #appliquer self.stat sur target
    for stat, value in self.stats.items():
      if stat == "hp":
        target.heal(value)
      elif stat == "attack":
        target._attack += value
      elif stat == "defense":
        target._defense += value

class Equipable(Item):
  def __init__(self, name, description, droprate, rarity, item_type, stats):
    super().__init__(name, description, droprate, rarity, item_type, stats)
