from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns

class View:
  def __init__(self):
    """Initialize the View class."""
    pass

  def inventory_view(self, list, team):
    console.print(Panel(f"Inventory View - List: {list} - Team: {team}")) 

  def use_item_view(self, item, target):
    print(f"Use Item View - Item: {item} - Target: {target}")
    
  def player_turn_view(self, team, character, enemies):
    print(f"Player Turn View - Team: {team} - Character: {character} - Enemies: {enemies}")

  def target_selection_view(self, team, character, enemies):
    print(f"Target Selection View - Team: {team} - Character: {character} - Enemies: {enemies}")

  def turn_info_view(self, team, event, enemies):
    team_txt = "\n".join(f"{c.name} - HP: {c.hp}/{c.max_hp}" for c in team)
    enemies_txt = "\n".join(f"{e.name} - HP: {e.hp}/{e.max_hp}" for e in enemies)

    box_team = self.display.create_info_box("Equipe", team_txt, "green", "white")
    box_event = self.display.create_info_box("Action", event, "yellow", "bold yellow")
    box_enemies = self.display.create_info_box("Ennemis", enemies_txt, "red", "white")

    self.display.display_view(Columns([box_team, box_event, box_enemies]))

  def team_selection_view(self, team, list_selection):
    print(f"Team Selection View - Team: {team} - Selection: {list_selection}")

  def title_screen_view(self):
    choix = int(input("Bienvune dans Morghul's de Rayan ! Souhitez-vous lancer le jeu(1), charger une partie(2), voir le classement(3) ou quitter(4) ?"))
    return choix

  def leaderboard_view(self, scores):
    table = Table(title="Leaderboard", border_style="yellow")
    table.add_column("#", justify="right", style="cyan")
    table.add_column("Joueur", style="bold white")
    table.add_column("Score", justify="right", style="green")
    for i, s in enumerate(scores, start=1):
      table.add_row(str(i), s["player_name"], str(s["score"]))

    self.display.display_view(table)

  def game_over_view(self):
    print("Game Over View")

  def load_game_view(self):
    print("Load Game View")

  def exit_view(self):
    print("Exit View")
