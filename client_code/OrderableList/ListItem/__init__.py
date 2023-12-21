from ._anvil_designer import ListItemTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from anvil_extras import augment

class ListItem(ListItemTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.item_box = TextBox()
    def edit_item_text(self, **event_args):
      self.item_box.remove_from_parent()

    self.item_box.add_event_handler('pressed_enter', edit_item_text)
    self.item_box.add_event_handler('lost_focus', edit_item_text)
    
    self.item_label.text = self.item_text
    for prop, val in properties.items():
      setattr(self.remove_button, prop, val)
    self.remove_button.visible = self.allow_remove

  @property
  def item_text(self):
    return self._item_text
  @item_text.setter
  def item_text(self, value):
    self._item_text = value
    self.item_label.item_text = value

  def remove_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.parent.parent.parent.parent.parent.remove_drag_item(self.index)
