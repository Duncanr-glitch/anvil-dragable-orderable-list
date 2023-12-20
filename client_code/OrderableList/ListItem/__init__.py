from ._anvil_designer import ListItemTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ListItem(ListItemTemplate):
  def __init__(self, item_text, index, allow_remove=True, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item_text = item_text
    self.index = index
    
    self.label_1.text = self.item_text
    for prop, val in properties.items():
      setattr(self.remove_button, prop, val)
    self.remove_button.visible = allow_remove

  @property
  def item_text(self):
    return self._item_text
  @item_text.setter
  def item_text(self, value):
    self._item_text = value
    self.label_1.item_text = value

  def remove_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.parent.parent.parent.parent.parent.remove_drag_item(self.index)
