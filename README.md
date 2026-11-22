# Morghul's Chronicles (V2)

Jeu de combat au tour par tour en ligne de commande, développé en Python avec stockage des données dans MongoDB.

## Fonctionnement

Au lancement, un menu interactif propose de démarrer une partie, d'afficher le classement ou de quitter.

Lors d'une partie, le joueur saisit un pseudo (3 à 13 caractères alphanumériques) puis sélectionne une équipe de 3 héros parmi 11 personnages disponibles. Le jeu enchaîne ensuite des vagues de combat contre un monstre tiré aléatoirement parmi 10 créatures. À chaque tour, les héros encore en vie attaquent le monstre, puis le monstre riposte sur un membre de l'équipe choisi au hasard. Les dégâts infligés correspondent à la différence entre l'attaque de l'attaquant et la défense de la cible (avec un minimum de 1).

La partie s'arrête lorsque toute l'équipe est vaincue. Le pseudo, le nombre de vagues atteintes et la composition de l'équipe sont alors enregistrés dans MongoDB pour alimenter le top 10 du classement.

## Stack technique

- Python 3.12 ou supérieur (utilise les f-strings avec guillemets imbriqués, testé avec Python 3.13 et 3.14)
- MongoDB (base locale `game_db`, collections `heroes`, `monsters` et `leaderboard`)
- `pymongo` pour l'accès à la base de données
- `rich` pour la mise en forme dans le terminal (bannière et tableaux)
- `InquirerPy` pour les menus et la sélection des héros

## Prérequis

- Python 3.12+
- Un serveur MongoDB local accessible sur `mongodb://localhost:27017`

## Installation et lancement

1. Cloner le dépôt :

```bash
git clone <url-du-depot>
cd Morghul-s-V2
```

2. Créer un environnement virtuel et installer les dépendances :

```bash
python -m venv .venv
# Sous Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Sous Linux / macOS
source .venv/bin/activate

pip install pymongo rich InquirerPy
```

3. S'assurer que le service MongoDB tourne en local, puis lancer le jeu :

```bash
python main.py
```

Au démarrage, `db_init.py` se connecte à MongoDB et réinitialise les collections `heroes` et `monsters` avec les données de base. Le classement (`leaderboard`) est conservé entre les parties.

## Structure du projet

- `main.py` : point d'entrée du programme et boucle du menu principal.
- `game.py` : déroulement des vagues, gestion des tours de combat et vérification de fin de partie.
- `models.py` : définition de la dataclass `Character` (statistiques, calcul des dégâts, état de vie).
- `db_init.py` : connexion à MongoDB (`game_db`), peuplement des héros et monstres, lecture et écriture du classement.
- `interfaces.py` : menus interactifs et tableaux dans le terminal avec `InquirerPy` et `rich`.
- `utils.py` : validation des entrées utilisateur, sélection aléatoire des monstres et fonctions utilitaires.
