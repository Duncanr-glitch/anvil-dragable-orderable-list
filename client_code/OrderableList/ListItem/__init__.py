from ._anvil_designer import ListItemTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ListItem(ListItemTemplate):
  def __init__(self, text, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.text = text
    self.label_1.text = self.text
    
