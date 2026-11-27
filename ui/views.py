from typing import Callable, List
from rich.panel import Panel
from rich.table import Table
from ui.display import Affichage
from core.entities import Character, Enemy
from core.items import Item
from db.models import SaveDB, ScoreDB

OPTIONS_TOUR = ["Attaquer", "Utiliser un objet", "Passer"]
OPTIONS_ECRAN_TITRE = ["Nouvelle Partie", "Charger Partie", "Leaderboard", "Quitter"]
OPTIONS_GAME_OVER = ["Retour à l'écran titre", "Quitter"]

RARITY_COLORS = {
  "commune": "white",
  "rare": "cyan",
  "épique": "magenta",
  "légendaire": "bold yellow",
}


def create_columns(cols, ratios=None) -> Table:
  if ratios is None:
    ratios = {1: [1], 2: [1, 1], 3: [2, 3, 2]}[len(cols)]

  grid = Table.grid(expand=True)
  for r in ratios:
    grid.add_column(ratio=r)
  grid.add_row(*cols)
  return grid


def _box_equipe(team: List[Character], titre="Équipe", border_style="blue", perso=None, selected_index=None) -> Panel:
  table = Table(expand=True, box=None, show_header=True, header_style="bold cyan")
  table.add_column("Héros", style="bold white")
  table.add_column("Stats", style="green")
  table.add_column("Équipement", style="yellow")

  if not team:
    table.add_row("[dim]Aucun héros[/]", "", "")
  else:
    for i, member in enumerate(team):
      is_selected = selected_index is not None and i == selected_index
      is_active = perso is not None and member == perso
      nom = f"❯ {member.name}" if (is_selected or is_active) else member.name
      stats = f"PV {member.hp}/{member.max_hp} | ATK {member.attack} | DEF {member.defense}"
      equip = ", ".join(item.name for item in member.equipment) if member.equipment else "Aucun"
      if is_selected:
        style = "bold yellow reverse"
      elif not member.is_alive():
        style = "dim"
      elif is_active:
        style = "bold cyan"
      else:
        style = ""
      table.add_row(nom, stats, equip, style=style)

  subtitle = "[dim]↑/↓ naviguer • ⏎ valider[/dim]" if selected_index is not None else None
  return Panel(
    table,
    title=f"[bold {border_style}]✦ {titre} ✦[/]",
    title_align="center",
    subtitle=subtitle,
    subtitle_align="center",
    border_style=border_style,
    height=Affichage.BOX_HEIGHT,
    expand=True,
    padding=(1, 1),
  )


def _box_ennemis(ennemis: List[Enemy], titre="Ennemis", border_style="red", selected_index=None) -> Panel:
  table = Table(expand=True, box=None, show_header=True, header_style="bold red")
  table.add_column("Ennemi", style="bold white")
  table.add_column("PV", style="red")
  table.add_column("ATK / DEF", style="yellow")

  if not ennemis:
    table.add_row("[dim]Aucun ennemi[/]", "", "")
  else:
    for i, enemy in enumerate(ennemis):
      is_selected = selected_index is not None and i == selected_index
      nom = f"❯ {enemy.name}" if is_selected else enemy.name
      pv = f"{enemy.hp}/{enemy.max_hp}"
      stats = f"ATK {enemy.attack} | DEF {enemy.defense}"
      if is_selected:
        style = "bold yellow reverse"
      elif not enemy.is_alive():
        style = "dim"
      else:
        style = ""
      table.add_row(nom, pv, stats, style=style)

  subtitle = "[dim]↑/↓ naviguer • ⏎ valider[/dim]" if selected_index is not None else None
  return Panel(
    table,
    title=f"[bold {border_style}]✦ {titre} ✦[/]",
    title_align="center",
    subtitle=subtitle,
    subtitle_align="center",
    border_style=border_style,
    height=Affichage.BOX_HEIGHT,
    expand=True,
    padding=(1, 1),
  )


def _box_objets(inventaire: List[Item], titre="Inventaire", border_style="blue", selected_index=None) -> Panel:
  table = Table(expand=True, box=None, show_header=True, header_style="bold cyan")
  table.add_column("Objet", style="bold white")
  table.add_column("Type", style="green")
  table.add_column("Rareté")

  if not inventaire:
    table.add_row("[dim]Inventaire vide[/]", "", "")
  else:
    for i, item in enumerate(inventaire):
      is_selected = selected_index is not None and i == selected_index
      nom = f"❯ {item.name}" if is_selected else item.name
      rarity_color = RARITY_COLORS.get(item.rarity, "white")
      rarity_txt = f"[{rarity_color}]{item.rarity}[/]"
      style = "bold yellow reverse" if is_selected else ""
      table.add_row(nom, item.item_type, rarity_txt, style=style)

  subtitle = "[dim]↑/↓ naviguer • ⏎ valider • Échap retour[/dim]" if selected_index is not None else None
  return Panel(
    table,
    title=f"[bold {border_style}]✦ {titre} ✦[/]",
    title_align="center",
    subtitle=subtitle,
    subtitle_align="center",
    border_style=border_style,
    height=Affichage.BOX_HEIGHT,
    expand=True,
    padding=(1, 1),
  )


def details_objet(objet: Item) -> str:
  lignes = [
    objet.name,
    objet.description,
    f"Type : {objet.item_type}",
    f"Rareté : {objet.rarity}",
  ]
  for stat, valeur in objet.stats.items():
    lignes.append(f"{stat} : {valeur:+d}")
  return "\n".join(lignes)


def details_sauvegarde(sauvegarde: SaveDB) -> str:
  lignes = [f"Joueur : {sauvegarde.player_name}", f"Score : {sauvegarde.score}"]
  lignes += ["", "Équipe"]
  lignes += [f"{perso.name} - PV {perso.hp}" for perso in sauvegarde.equipe]
  lignes += ["", "Monstres"]
  lignes += [f"{monstre.name} - PV {monstre.hp}" for monstre in sauvegarde.monsters]
  lignes += ["", "Inventaire"]
  lignes += [objet.name for objet in sauvegarde.inventaire] or ["Vide"]
  return "\n".join(lignes)


def VueInventaire(inventaire: List[Item], team: List[Character]) -> Callable:
  def create_details_info(index: int) -> str:
    if not inventaire:
      return "Inventaire vide"
    return details_objet(inventaire[index])

  def inner_VueInventaire(index: int):
    selected_box = _box_objets(inventaire, titre="Inventaire", border_style="blue", selected_index=index)
    details = Affichage.create_info_box(
      titre="Détails",
      info=create_details_info(index),
      box_color="magenta",
      text_color="white",
    )
    team_box = _box_equipe(team, titre="Équipe", border_style="green")
    return create_columns([selected_box, details, team_box], ratios=[3, 2, 4])

  return inner_VueInventaire


def VueSelectionCibleObjet(objet: Item, team: List[Character]) -> Callable:
  def inner_VueSelectionCibleObjet(index: int):
    selected_box = _box_equipe(
      team,
      titre=f"Choisir une cible pour {objet.name}",
      border_style="blue",
      selected_index=index,
    )
    details = Affichage.create_info_box(
      titre="Détails de l'objet",
      info=details_objet(objet),
      box_color="magenta",
      text_color="white",
    )
    return create_columns([selected_box, details], ratios=[3, 2])

  return inner_VueSelectionCibleObjet


def VueTourJoueur(team: List[Character], perso: Character, ennemis: List[Enemy]) -> Callable:
  def inner_VueTourJoueur(index: int):
    team_box = _box_equipe(team, titre=f"Tour de {perso.name}", border_style="blue", perso=perso)
    actions_box = Affichage.create_select_box(
      titre="Choix d'action",
      items=OPTIONS_TOUR,
      index=index,
      box_color="magenta",
      text_color="white",
      hover_color="yellow",
    )
    ennemis_box = _box_ennemis(ennemis, titre="Ennemis", border_style="red")
    return create_columns([team_box, actions_box, ennemis_box], ratios=[4, 2, 3])

  return inner_VueTourJoueur


def VueChoixCible(team: List[Character], perso: Character, ennemis: List[Enemy]) -> Callable:
  def inner_VueChoixCible(index: int):
    team_box = _box_equipe(team, titre=f"Tour de {perso.name}", border_style="blue", perso=perso)
    dmg = perso.project_damage(ennemis[index])
    details = Affichage.create_info_box(
      titre="Projection des dégâts",
      info=f"{perso.name} ➔ {ennemis[index].name}\n\nDégâts estimés : {dmg}",
      box_color="magenta",
      text_color="white",
    )
    selected_box = _box_ennemis(
      ennemis,
      titre=f"Cible pour {perso.name}",
      border_style="red",
      selected_index=index,
    )
    return create_columns([team_box, details, selected_box], ratios=[4, 2, 3])

  return inner_VueChoixCible


def VueInfoTour(team: List[Character], event: str, ennemis: List[Enemy]) -> Callable:
  def inner_VueInfoTour(index: int):
    team_box = _box_equipe(team, titre="Équipe", border_style="blue")
    event_box = Affichage.create_info_box(
      titre="Événement",
      info=event,
      box_color="magenta",
      text_color="white",
    )
    ennemis_box = _box_ennemis(ennemis, titre="Ennemis", border_style="red")
    return create_columns([team_box, event_box, ennemis_box], ratios=[4, 2, 3])

  return inner_VueInfoTour


def VueSelectionEquipe(team: List[Character], listSelection: List[Character]) -> Callable:
  def inner_VueSelectionEquipe(index: int):
    team_box = _box_equipe(team, titre=f"Équipe ({len(team)}/3)", border_style="blue")
    selection_box = _box_equipe(
      listSelection,
      titre="Sélection de l'équipe",
      border_style="magenta",
      selected_index=index,
    )
    return create_columns([team_box, selection_box], ratios=[2, 3])

  return inner_VueSelectionEquipe


def VueEcranTitre() -> Callable:
  def inner_VueEcranTitre(index: int):
    return Affichage.create_select_box(
      titre="Morghul's Chronicles",
      items=OPTIONS_ECRAN_TITRE,
      index=index,
      box_color="cyan",
      text_color="white",
      hover_color="yellow",
    )

  return inner_VueEcranTitre


def VueLeaderboard(scores: List[ScoreDB]) -> Callable:
  def inner_VueLeaderboard(index: int):
    table = Table(expand=True, box=None, show_header=True, header_style="bold yellow")
    table.add_column("#", justify="right", style="cyan", width=4)
    table.add_column("Joueur", style="bold white")
    table.add_column("Score", justify="right", style="green")

    if not scores:
      table.add_row("", "[dim]Aucun score enregistré[/]", "")
    else:
      for rang, score in enumerate(scores, start=1):
        table.add_row(str(rang), score.player_name, str(score.score))

    return Panel(
      table,
      title="[bold yellow]✦ Leaderboard ✦[/]",
      title_align="center",
      subtitle="[dim]⏎ retour[/dim]",
      subtitle_align="center",
      border_style="yellow",
      height=Affichage.BOX_HEIGHT,
      expand=True,
      padding=(1, 2),
    )

  return inner_VueLeaderboard


def VueGameOver() -> Callable:
  def inner_VueGameOver(index: int):
    return Affichage.create_select_box(
      titre="Game Over",
      items=OPTIONS_GAME_OVER,
      index=index,
      box_color="red",
      text_color="white",
      hover_color="yellow",
    )

  return inner_VueGameOver


def VueChargerSauvegarde(sauvegardes: List[SaveDB]) -> Callable:
  def create_details_info(index: int) -> str:
    if not sauvegardes:
      return "Aucune sauvegarde disponible"
    return details_sauvegarde(sauvegardes[index])

  def inner_VueChargerSauvegarde(index: int):
    selected_box = Affichage.create_select_box(
      titre="Charger une sauvegarde",
      items=[f"{save.player_name} - Score {save.score}" for save in sauvegardes],
      index=index,
      box_color="blue",
      text_color="white",
      hover_color="yellow",
    )
    details = Affichage.create_info_box(
      titre="Détails",
      info=create_details_info(index),
      box_color="magenta",
      text_color="white",
    )
    return create_columns([selected_box, details])

  return inner_VueChargerSauvegarde


def VueQuitter() -> Callable:
  def inner_VueQuitter(index: int) -> Panel:
    return Affichage.create_info_box(
      titre="Quitter",
      info="Merci d'avoir joué ! À bientôt.",
      box_color="red",
      text_color="white",
    )

  return inner_VueQuitter
