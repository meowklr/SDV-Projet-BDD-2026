from rich.console import Console
from rich.panel import Panel

class Display:
  def __init__(self):
    self.console = Console()
    self.console.clear()

  def display_view(self, renderable):
    self.console.clear()
    self.console.print(renderable)

  def show_error(self, error_message):
    self.console.print(
      Panel(error_message, title="Erreur", border_style="red", style="bold red")
    )

  def create_info_box(self, title, info, box_color, text_color):
    return Panel(
      f"[{text_color}]{info}[/]",
      title=title,
      border_style=box_color,
      expand=True,
    )

  def create_select_box(self, title, items, index, box_color, text_color, hover_color):
    lines = []
    for i, item in enumerate(items):
      if i == index:
        lines.append(f"[{hover_color}] > {i + 1}. {item} [/]")
      else:
        lines.append(f"[{text_color}]   {i + 1}. {item}[/]")
    return Panel(
      "\n".join(lines),
      title=title,
      border_style=box_color,
      expand=True,
    )