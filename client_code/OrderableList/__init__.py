from ._anvil_designer import OrderableListTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..DragableList import DragableList, DRAGABLE_LIST_CHANGE_EVENT
from ..ListItem import ListItem

class OrderableList(OrderableListTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self._dragable_list = DragableList()
    self._dragable_list.set_event_handler(DRAGABLE_LIST_CHANGE_EVENT, self._list_changed)
    self.list_panel.add_component(self._dragable_list)
    
  def _list_changed(self, **eventargs):
    self.order_label.text = f'Order = {[comp.get_text() for comp in self._dragable_list.get_sorted_components()]}'
    

  def add_drag_item(self, text):
    """This method is called when the column panel is shown on the screen"""
    comps = self._dragable_list.get_sorted_components()    
    comps.append(ListItem(text=text))
    self._dragable_list.components = comps
    self._dragable_list.refresh()
    pass

  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    self.add_drag_item("hello world!")
#     self.add_drag_item("again!")
    pass



