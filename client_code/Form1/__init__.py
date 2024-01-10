from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..OrderableList.ListItem import ListItem

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.orderable_list_1.remove_button_properties = {
      "background": "red",
      "foreground": "yellow"
    }

    # Any code you write here will run when the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    # self.orderable_list_1.add_drag_item([f"{self.text_box_1.text}: {i}" for i in range(3)])
    self.orderable_list_1.add_drag_item(self.text_box_1.text)

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.orderable_list_1.remove_drag_item([int(ind) for ind in self.text_box_2.text.split(",")])

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.orderable_list_1.remove_button_properties = {
      "background": "yellow",
      "foreground": "red"
    }

  def orderable_list_1_list_changed(self, **event_args):
    """This method is called when the length or order of the list change"""
    # print(self.orderable_list_1._dragable_list.components)
    pass

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.orderable_list_1.components = [ListItem(item_text="Hello world", index=0)]

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    self.orderable_list_1.components = [ListItem(item_text="Hello Init", index=0)]


