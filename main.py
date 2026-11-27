from core.player import Player
from core.game import Game
from ui.display import Affichage
from ui.views import OPTIONS_ECRAN_TITRE, VueEcranTitre, VueQuitter


def main():
  while True:
    start_choice = Affichage.display_vue(VueEcranTitre(), max_index=len(OPTIONS_ECRAN_TITRE))
    if start_choice == 0:
      player_name = Affichage.demander_input("Entrez votre nom de joueur : ").strip()
      player = Player(player_name)
      game = Game(player)
      player.create_team(game.load_characters())
      game.launch_game()
    elif start_choice == 1:
      game = Game(None)
      game.load_game()
    elif start_choice == 2:
      game = Game(None)
      game.show_leaderboard()
      game.client.close()
    elif start_choice in (3, None):
      Affichage.display_vue(VueQuitter())
      break


if __name__ == "__main__":
  main()
