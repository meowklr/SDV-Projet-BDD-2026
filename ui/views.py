class View:
  """Affichages à appeler depuis le contrôleur du jeu.

  Exemple d'utilisation dans le contrôleur :
      view = View()
      view.title_screen_view()
      view.player_turn_view(team, character, enemies)

  Remplace progressivement les appels à print par l'interface graphique
  ou les interactions console souhaitées.
  """

  def __init__(self):
    """Initialize the View class."""
    pass

  def inventory_view(self, list, team):
    print(f"Inventory View - {list} - Team: {team}")

  def use_item_view(self, item, target):
    print(f"Use Item View - Item: {item} - Target: {target}")
    
  def player_turn_view(self, team, character, enemies):
    print(f"Player Turn View - Team: {team} - Character: {character} - Enemies: {enemies}")

  def target_selection_view(self, team, character, enemies):
    print(f"Target Selection View - Team: {team} - Character: {character} - Enemies: {enemies}")

  def turn_info_view(self, team, event, enemies):
    print(f"Turn Info View - Team: {team} - Event: {event} - Enemies: {enemies}")

  def team_selection_view(self, team, list_selection):
    print(f"Team Selection View - Team: {team} - Selection: {list_selection}")

  def title_screen_view(self):
    choix = int(input("Bienvune dans Morghul's de Rayan ! Souhitez-vous lancer le jeu(1), charger une partie(2), voir le classement(3) ou quitter(4) ?"))
    return choix

  def leaderboard_view(self, scores):
    print(f"Leaderboard View - Scores: {scores}")

  def game_over_view(self):
    print("Game Over View")

  def load_game_view(self):
    print("Load Game View")

  def exit_view(self):
    print("Exit View")
