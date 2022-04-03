from ._anvil_designer import OrderableListTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .DragableList import DragableList, DRAGABLE_LIST_CHANGE_EVENT
from .ListItem import ListItem
from anvil_extras.utils._component_helpers import _html_injector


class OrderableList(OrderableListTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self._dragable_list = DragableList()
    self._dragable_list.set_event_handler(DRAGABLE_LIST_CHANGE_EVENT, self._list_changed)
    self.list_panel.add_component(self._dragable_list)
    
    
  def _list_changed(self, **eventargs):
    self.order_label.text = f'{self.order_title} = {self.get_ordered_comps()}'
    self.raise_event("list_changed")
    
  def get_ordered_comps(self):
    """Method to get the sorted list with each item's text"""
    return [comp.get_text() for comp in self._dragable_list.get_sorted_components()]
    
  def add_drag_item(self, text):
    """Method to add items to the draggable list"""
    comps = self._dragable_list.get_sorted_components()    
    comps.append(ListItem(text=text))
    self._dragable_list.components = comps

  def remove_drag_item(self, index):
    """Method to remove items from the draggable list"""
    comps = self._dragable_list.get_sorted_components()
    comps.remove(comps[index])
    self._dragable_list.components = comps
    
  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    _html_injector.css("""/* Roles for muuri */ 
  .anvil-role-grid {
  position: relative;
  overflow: hidden;
  min-height: 20vh;
  }
  .anvil-role-item {
  display: block;
  position: absolute;
  margin: 0px;
  width: 100%;
  z-index: 1;
  }
  .anvil-role-item.muuri-item-dragging {
  z-index: 3;
  }
  .anvil-role-item.muuri-item-releasing {
  z-index: 2;
  }
  .anvil-role-item.muuri-item-hidden {
  z-index: 0;
  }""")


