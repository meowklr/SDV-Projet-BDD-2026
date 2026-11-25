#vague
class Vague:
  def __init__(self, current_vague, enemies):
    self.current_vague = current_vague
    self.enemies = enemies

  def pick_enemies(self, current_vague):
    # Logic to pick enemies based on the current wave
    pass


  def play_vague(self, player):
    for enemy in self.enemies:
      while enemy.is_alive() and player.is_alive():
        player.play_turn(enemy)
        if enemy.is_alive():
          enemy.play_turn(player)

  def get_difficulty(self):
    # Logic to determine the difficulty of the wave based on the wave number
    difficulty = self.current_vague
    return difficulty