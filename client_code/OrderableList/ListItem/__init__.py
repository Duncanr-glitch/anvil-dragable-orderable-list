from ._anvil_designer import ListItemTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ListItem(ListItemTemplate):
  def __init__(self, text, index, allow_remove=True, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.text = text
    self.index = index
    
    self.label_1.text = self.text
    self.remove_button.visible = allow_remove

  @property
  def text(self):
    return self._text
  @text.setter
  def text(self, value):
    self._text = value
    self.label_1.text = value

  def remove_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.parent.parent.parent.parent.parent.remove_drag_item(self.index)
