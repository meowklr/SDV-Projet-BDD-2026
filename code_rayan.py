import copy
import os
import random
from time import sleep

import pymongo
from InquirerPy import inquirer
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel


TEAM_SIZE = 3
TOP_SCORES_COUNT = 3

MENU = [
  "Lancer Jeu",
  "Afficher LeaderBoard",
  "Quitter",
]

console = Console()
client = pymongo.MongoClient(os.getenv("MONGO_URL"))


class Joueur:
  def __init__(self, name):
    self.name = name
    self.waves = 0
    self.actual_wave = 0

  def to_db_score(self):
    return {"player_name": self.name, "score": self.waves}


def afficher_score(joueur):
  print(f"Score de {joueur.name}: {joueur.waves}")


def creer_joueur(db):
  nom_joueur = recuperer_nom_valide(db)
  return Joueur(nom_joueur)


def recuperer_nom_valide(db):
  while True:
    nom = input("Entrez le nom du joueur: ").strip()
    if est_nom_valide(nom, db):
      return nom
    print("Nom invalide ou déjà utilisé, veuillez réessayer.")


def est_nom_valide(nom, db):
  if len(nom) < 3 or len(nom) > 20:
    return False
  if not est_nom_unique(nom, db):
    return False
  return True


def est_nom_unique(nom, db):
  return db["scores"].find_one({"player_name": nom}) is None


def creer_equipe(db):
  persos_db = recuperer_persos_db(db)
  equipe = []
  while not est_equipe_complete(equipe):
    persos_dispo = creer_liste_persos_dispo(persos_db, equipe)
    choix = get_perso_choice(persos_dispo)
    equipe.append(persos_dispo[choix - 1])
  return equipe


def creer_liste_persos_dispo(persos_db, equipe):
  persos_dispo = persos_db.copy()
  for perso in equipe:
    if perso in persos_dispo:
      persos_dispo.remove(perso)
  return persos_dispo


def est_equipe_complete(equipe):
  return len(equipe) >= TEAM_SIZE


def recuperer_persos_db(db):
  return list(db["characters"].find())


def create_perso_message(perso):
  return f"{perso['name']} - ATK : {perso['attack']} - HP : {perso['hp']} - DEF : {perso['defense']}"


def create_persos_message():
  return "Choisissez un perso parmi les suivants:"


def get_perso_choice(persos):
  message = create_persos_message()
  persos_choice = [create_perso_message(perso) for perso in persos]
  return get_valid_choice(message, persos_choice)


def recuperer_monstres_db(db):
  return list(db["monsters"].find())


def est_entite_en_vie(entite):
  return entite["hp"] > 0


def est_equipe_en_vie(equipe):
  return any(est_entite_en_vie(membre) for membre in equipe)


def selectionner_monstre_aleatoire(monstres):
  return copy_entity(random.choice(monstres))


def recuperer_membres_en_vie(equipe):
  return [membre for membre in equipe if est_entite_en_vie(membre)]


def equipe_attaque_monstre(membres_en_vie, monstre):
  evenements = []
  for membre in membres_en_vie:
    if est_entite_en_vie(monstre):
      evenements.append({
        "message": infliger_degats(membre, monstre),
        "team": copy_team(membres_en_vie),
        "monster": copy_entity(monstre),
      })
  return evenements


def choose_target_in_team(equipe):
  return random.choice(equipe)


def infliger_degats(atk, defn):
  degats = max(atk["attack"] - defn["defense"], 1)
  defn["hp"] = max(defn["hp"] - degats, 0)
  return f"{atk['name']} inflige {degats} degats a {defn['name']}"


def copy_entity(entite):
  return copy.deepcopy(entite)


def copy_team(equipe):
  return [copy_entity(membre) for membre in equipe]


def monstre_attaque_equipe(monstre, equipe):
  if not est_entite_en_vie(monstre):
    return []
  membres_en_vie = recuperer_membres_en_vie(equipe)
  target = choose_target_in_team(membres_en_vie)
  return [{
    "message": infliger_degats(monstre, target),
    "monster": copy_entity(monstre),
    "team": copy_team(equipe),
  }]


def lancer_vague(joueur, equipe, monstre):
  while est_entite_en_vie(monstre) and est_equipe_en_vie(equipe):
    evenements = []
    membres_en_vie = recuperer_membres_en_vie(equipe)

    evenements += equipe_attaque_monstre(membres_en_vie, monstre)
    evenements += monstre_attaque_equipe(monstre, equipe)

    afficher_evenements(joueur, evenements)

  return est_equipe_en_vie(equipe)


def creer_titre_tour(player):
  title = f"Tour de {player.name} - Vague {player.actual_wave}"
  return Panel(
    Align.center(title, style="bold blue"),
    border_style="blue",
  )


def creer_text_equipe(equipe):
  return "\n".join(f"{membre['name']} - HP: {membre['hp']}" for membre in equipe)


def creer_team_panel(equipe):
  text_equipe = creer_text_equipe(equipe)
  return Panel(text_equipe, title="🟢 Equipe", border_style="green", expand=True)


def creer_text_monstre(monstre):
  return f"{monstre['name']} - HP: {monstre['hp']}"


def creer_monstre_panel(monstre):
  text_monstre = creer_text_monstre(monstre)
  return Panel(text_monstre, title="🔴 Monstre", border_style="red", expand=True)


def creer_infos_panel(evenement):
  return Panel(evenement["message"], title="Infos", border_style="yellow", expand=True)


def afficher_evenements(player, evenements):
  titre_tour = creer_titre_tour(player)
  for evenement in evenements:
    clear_console()

    team = creer_team_panel(evenement["team"])
    monster = creer_monstre_panel(evenement["monster"])
    infos = creer_infos_panel(evenement)
    console.print(titre_tour)
    console.print(Columns([team, infos, monster]))

    sleep(2)


def lancer_combat_a_mort(db, joueur, equipe):
  monstres = recuperer_monstres_db(db)
  joueur.actual_wave = 1
  while est_equipe_en_vie(equipe):
    monstre = selectionner_monstre_aleatoire(monstres)
    victoire = lancer_vague(joueur, equipe, monstre)
    if victoire:
      joueur.actual_wave += 1
  return joueur.actual_wave


def enregistrer_score(db, score):
  db.scores.insert_one(score)


def lancer_jeu(db):
  joueur = creer_joueur(db)

  while True:
    equipe = creer_equipe(db)
    waves = lancer_combat_a_mort(db, joueur, equipe)
    joueur.waves = waves
    afficher_score(joueur)
    afficher_leaderboard_joueur(db, joueur.to_db_score())
    if not replay():
      break
  enregistrer_score(db, joueur.to_db_score())


def replay():
  choice = get_valid_choice("Voulez-vous rejouer ?", ["1. Oui", "2. Non"])
  return choice == 1


def clear_console():
  # 'nt' correspond à Windows, 'posix' correspond à Linux et macOS
  os.system("cls" if os.name == "nt" else "clear")


def create_menu_message():
  return "Entrez votre choix: "


def get_valid_choice(message, options):
  clear_console()
  choice = inquirer.select(
    message=message,
    choices=options,
  ).execute()
  return options.index(choice) + 1


def get_menu_choice():
  return get_valid_choice(create_menu_message(), MENU)


def connect_db():
  return client["game_db"]


def close_db():
  client.close()


def lancer_processus(choice, db):
  if choice == 1:
    lancer_jeu(db)
  elif choice == 2:
    afficher_leaderboard(db)
  elif choice == 3:
    close_db()
    print("Fermeture du programme")
    exit()
  else:
    print("Choix invalide")


def get_score_value(score_doc):
  return score_doc.get("score", score_doc.get("waves", 0))


def get_sorted_scores(list_scores):
  return sorted(list_scores, key=get_score_value, reverse=True)


def afficher_scores(scores):
  for score in scores:
    print(f"{score['player_name']} : {get_score_value(score)}")
  sleep(0.5)


def get_top_scores(list_scores):
  return get_sorted_scores(list_scores)[:TOP_SCORES_COUNT]


def get_score_db(db):
  return list(db.scores.find())


def afficher_leaderboard(db):
  scores_db = get_score_db(db)
  scores = get_top_scores(scores_db)
  afficher_scores(scores)


def afficher_leaderboard_joueur(db, player):
  scores_db = get_score_db(db)
  scores_db.append(player)
  scores = get_top_scores(scores_db)
  afficher_scores(scores)


def main():
  db = connect_db()
  while True:
    choice = get_menu_choice()
    lancer_processus(choice, db)


if __name__ == "__main__":
  main()
