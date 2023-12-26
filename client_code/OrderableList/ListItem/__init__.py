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
    self.editable = False
    self.allow_remove = False
    
    self.item_edit_card = ColumnPanel(role="card")
    self.item_box = TextBox(role="inline-popup")
    self.item_edit_card.add_component(self.item_box)

    self.item_box.add_event_handler('pressed_enter', self.set_edited_item_text)
    self.item_box.add_event_handler('lost_focus', self.set_edited_item_text)
    augment.set_event_handler(self.item_box, "keydown", self.clear_item_changes)
    
    self.item_label.text = self.item_text
    for prop, val in properties.items():
      setattr(self.remove_button, prop, val)

  @property
  def item_text(self):
    return self._item_text
  @item_text.setter
  def item_text(self, value):
    self._item_text = value
    self.item_label.text = value

  @property
  def editable(self):
    return self._editable
  @editable.setter
  def editable(self, value):
    self._editable = value
    if value:
      augment.set_event_handler(self.item_lbl_card, "dblclick", self.start_edit_item_text)
    else:
      try:
        augment.remove_event_handler(self.item_lbl_card, "dblclick", self.start_edit_item_text)
      except (ValueError, LookupError):
        print("Event doesn't exist, skipping")

  @property
  def allow_remove(self):
    return self._allow_remove
  @allow_remove.setter
  def allow_remove(self, value):
    self._allow_remove = value
    self.remove_button.visible = value

  def remove_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    confirm_remove = True
    if self.orderable_list.confirm_removal:
      confirm_remove = confirm(self.orderable_list.removal_alert_message.replace("{item_text}", "self.item_text"))

    if confirm_remove:
      self.orderable_list.remove_drag_item(self.index)

  def start_edit_item_text(self, **event_args):
    self.item_lbl_card.remove_from_parent()
    self.add_component(self.item_edit_card)
    self.item_box.focus()
    self.item_box.text = self.orderable_list._get_list_item_value(self)

  def _reset_editing_state(self, **event_args):
    self.item_edit_card.remove_from_parent()
    self.add_component(self.item_lbl_card)
    
  def set_edited_item_text(self, **event_args):
    try:
      self._reset_editing_state()
      if self.orderable_list.numeration:
        self.item_text = f"{self.item_label.text.split('. ')[0]}. {self.item_box.text}"
      else:
        self.item_text = self.item_box.text
    except ValueError:
      # This is for preventing both lost_focus and pressed_enter triggering
      pass

  def clear_item_changes(self, **event_args):
    if event_args["key"] == "Escape":
      self._reset_editing_state()
  
  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    self.orderable_list = self.parent.parent.parent.parent.parent.parent
    print(self.orderable_list.__name__)
    self.editable = self.orderable_list.item_editable
    self.allow_remove = self.orderable_list.allow_remove
