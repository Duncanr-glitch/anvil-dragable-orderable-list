from ._anvil_designer import muuri_htmlTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import document, Muuri

class muuri_html(muuri_htmlTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    grid_1 = Muuri('.grid-1', {
    'dragEnabled': True,
    'dragContainer': document.body,
    'dragSort': lambda: [grid_1, grid_2]
  })
  grid_2 = Muuri('.grid-1', {
    'dragEnabled': True,
    'dragContainer': document.body,
    'dragSort': lambda: [grid_1, grid_2]
  })
