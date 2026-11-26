from core.player import Player
from core.game import Game
from ui.views import View


def main():
  view = View()
  start_choice = view.title_screen_view()
  if start_choice == 1:
    player_name = input("Entrez votre nom de joueur : ").strip()
    player = Player(player_name)
    game = Game(player)
    player.create_team(game.load_characters())
    game.launch_game()
  elif start_choice == 2:
    game = Game(None)
    game.load_game()
  elif start_choice == 3:
    game = Game(None)
    game.show_leaderboard()
  elif start_choice == 4:
    view.exit_view()


if __name__ == "__main__":
  main()
