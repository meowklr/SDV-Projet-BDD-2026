from rich.console import Console


class Display:
  def __init__(self):
    self.console = Console()
    self.console.clear()

  def display_view(self, renderable):
    self.console.clear()
    self.console.print(renderable)

  def show_error(self, error_message):
    print(f"Error: {error_message}")

  def create_info_box(self, title, info, box_color, text_color):
    # logic to create an info box with the given parameters
    pass

  def create_select_box(self, title, items, index, box_color, text_color, hover_color):
    # logic to create a select box with the given parameters
    pass
