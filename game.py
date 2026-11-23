import copy
import os
from random import choice
from time import sleep

from pymongo import MongoClient
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

LAYOUT = Layout()
console = Console()

TAILLE_MAX_EQUIPE = 3
MENU = ["Jouer", "Leaderboard", "Quitter"]
BANNED_PSEUDOS = {"admin", "root", "superuser"}

LAYOUT.split_row(
    Layout(name="left", ratio=2),
    Layout(name="center", ratio=3),
    Layout(name="right", ratio=2),
)


def create_panel(title="", text="", color="yellow"):
    return Panel(
        Align.center(f"[{color}]{text}[/{color}]", vertical="middle"),
        title=title,
        border_style=color,
    )


def choix_menu():
    message = "Veuillez choisir une option :"
    return get_user_choice_from_options(MENU, message)


def lancer_processus(choix):
    if choix == 1:
        lancer_jeu()
    elif choix == 2:
        print("Leaderboard non implémenté.")
    elif choix == 3:
        print("Au revoir !")


def main():
    choix = choix_menu()
    lancer_processus(choix)


def afficher_game_over(equipe, score):
    print("Game Over !")
    print(f"Votre équipe a survécu à {score} vagues.")
    print("Statut final de l'équipe :")
    for hero in equipe:
        print(f"{hero['name']} - HP: {hero['hp']}")


def lancer_jeu():
    db = connect_db()
    pseudo = get_username(db)
    heros_disponibles = recuperer_all_heroes(db)
    monstres = recuperer_all_monsters(db)
    equipe = create_team(heros_disponibles)
    score = combat_a_mort(equipe, monstres)
    afficher_game_over(equipe, score)
    enregistrer_resultat_combat(db, pseudo, score)


def enregistrer_resultat_combat(db, pseudo, score):
    db["scores"].insert_one({
        "player_name": pseudo,
        "waves": score,
    })


def recuperer_all_heroes(db):
    return list(db["characters"].find())


def recuperer_all_monsters(db):
    return list(db["monsters"].find())


def connect_db():
    client = MongoClient(os.getenv("MONGO_URL"))
    return client["game_db"]


def est_entite_en_vie(entite):
    return entite["hp"] > 0


def est_equipe_en_vie(equipe):
    return any(est_entite_en_vie(hero) for hero in equipe)


def selectionner_monstre(monstres):
    monstre_choice = choice(monstres)
    return copy.deepcopy(monstre_choice)


def combat_a_mort(equipe, monstres):
    vague = 1
    while est_equipe_en_vie(equipe):
        monstre = selectionner_monstre(monstres)
        victoire = lancer_vague(equipe, monstre)
        if victoire:
            print(f"Victoire pour la vague {vague} !")
            vague += 1
    return vague


def lancer_vague(equipe, monstre):
    while est_entite_en_vie(monstre) and est_equipe_en_vie(equipe):
        evenements = tour_de_vague(equipe, monstre)
        afficher_evenements(evenements, equipe, monstre)
        sleep(1)
    return est_equipe_en_vie(equipe)


def update_layout(equipe_panel, monstre_panel, info_panel):
    LAYOUT["left"].update(equipe_panel)
    LAYOUT["right"].update(monstre_panel)
    LAYOUT["center"].update(info_panel)


def afficher_evenements(evenements, equipe, monstre):
    console.clear()
    print("\n\n")

    equipe_panel = create_panel(
        "Equipe",
        "\n".join(f"{hero['name']} - HP: {hero['hp']}" for hero in equipe),
        "green",
    )
    monstre_panel = create_panel(
        "Monstre",
        f"{monstre['name']} - HP: {monstre['hp']}",
        "red",
    )
    info_panel = create_panel("Evenements", "\n".join(evenements), "yellow")

    update_layout(equipe_panel, monstre_panel, info_panel)
    console.print(LAYOUT, height=10)


def tour_de_vague(equipe, monstre):
    evenements = []
    evenements += tour_utilisateur(equipe, monstre)
    if est_entite_en_vie(monstre):
        evenements += tour_monstre(equipe, monstre)
    return evenements


def tour_monstre(equipe, monstre):
    cible = recuperer_cible(equipe)
    degat = attaquer(monstre, cible)
    return [f"{monstre['name']} inflige {degat} degats a {cible['name']}"]


def attaquer(attacker, cible):
    degat = min(calculer_degats(attacker, cible), cible["hp"])
    cible["hp"] -= degat
    return degat


def calculer_degats(attacker, cible):
    return max(1, attacker["attack"] - cible["defense"])


def recuperer_cible(equipe):
    cible_potentielle = recuperer_heros_en_vie(equipe)
    return choice(cible_potentielle)


def recuperer_heros_en_vie(equipe):
    return [hero for hero in equipe if est_entite_en_vie(hero)]


def tour_utilisateur(equipe, monstre):
    evenements = []
    for hero in recuperer_heros_en_vie(equipe):
        evenements += tour_perso_jouable(hero, monstre)
    return evenements


def tour_perso_jouable(hero, monstre):
    if est_entite_en_vie(monstre):
        degat = attaquer(hero, monstre)
        return [f"{hero['name']} inflige {degat} degats a {monstre['name']}"]
    return []


def create_team(heroes):
    equipe = []
    while not equipe_est_complete(equipe):
        afficher_equipe_actuelle(equipe)
        heros_dispo = calculer_heros_disponibles(equipe, heroes)
        options = construire_options(heros_dispo)
        choix = get_user_choice_from_options(options, "Choisissez un héros : ")
        selected_hero = copy.deepcopy(heros_dispo[choix - 1])
        equipe.append(selected_hero)
    return equipe


def equipe_est_complete(equipe):
    return len(equipe) >= TAILLE_MAX_EQUIPE


def hero_to_string(hero):
    return (
        f"{hero['name']} - ATK : {hero['attack']} "
        f"- HP : {hero['hp']} - DEF : {hero['defense']}"
    )


def construire_options(liste_heros_dispo):
    return [hero_to_string(hero) for hero in liste_heros_dispo]


def calculer_heros_disponibles(equipe, liste_heros):
    return [hero for hero in liste_heros if hero not in equipe]


def afficher_personnage(personnage):
    print(hero_to_string(personnage))


def afficher_equipe_actuelle(equipe):
    for i in range(TAILLE_MAX_EQUIPE):
        if i < len(equipe):
            afficher_personnage(equipe[i])
        else:
            print("Vide")


def get_username(db):
    while True:
        pseudo = input("Entrez votre pseudo : ").strip()
        if validate_username(pseudo, db):
            return pseudo
        print("Pseudo invalide, veuillez réessayer.")


def validate_username(pseudo, db):
    return (
        3 <= len(pseudo) <= 20
        and pseudo not in BANNED_PSEUDOS
        and not is_username_in_db(pseudo, db)
    )


def is_username_in_db(pseudo, db):
    return db["scores"].find_one({"player_name": pseudo}) is not None


def get_user_choice_from_options(options, message):
    while True:
        print(message)
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")
        choix = input("Entrez votre choix : ").strip()
        if validate_user_choice(choix, 1, len(options)):
            return int(choix)
        print("Choix invalide, veuillez réessayer.")


def validate_user_choice(choix, minimum, maximum):
    if not choix.isdigit():
        return False
    return minimum <= int(choix) <= maximum


if __name__ == "__main__":
    main()