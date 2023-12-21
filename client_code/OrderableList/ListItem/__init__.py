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
    augment.set_event_handler(self.item_label, "dblclick", self.start_edit_item_text)

    self.item_edit_card = ColumnPanel(role="card")
    self.item_box = TextBox()
    self.item_edit_card.add_component(self.item_box)

    self.item_box.add_event_handler('pressed_enter', self.set_edited_item_text)
    self.item_box.add_event_handler('lost_focus', self.set_edited_item_text)
    
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
    self.orderable_list.remove_drag_item(self.index)
  def start_edit_item_text(self, **event_args):
    self.item_lbl_card.remove_from_parent()
    self.add_component(self.item_edit_card)
    self.item_box.focus()
    self.item_box.text = self.orderable_list._get_list_item_value(self)
    
  def set_edited_item_text(self, **event_args):
    try:
      self.item_edit_card.remove_from_parent()
      self.add_component(self.item_lbl_card)
    except ValueError:
      # This is for preventing both lost_focus and pressed_enter triggering
      pass

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    self.orderable_list = self.parent.parent.parent.parent.parent
