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
    self._dragable_list = DragableList(drag_enabled=True)
    self.init_components(**properties)
    self._dragable_list.drag_enabled = self.drag_enabled
    self._dragable_list.set_event_handler(DRAGABLE_LIST_CHANGE_EVENT, self._list_changed)
    self.list_panel.add_component(self._dragable_list)
    
    self.adding = False
    self.rendered = False

  @property
  def components(self):
    return self._dragable_list.components
  @components.setter
  def components(self, value):
    list_item_check = [isinstance(comp, ListItem) for comp in value or []]
    is_all_list_items = all(list_item_check)
    is_any_list_items = any(list_item_check)
    if is_all_list_items:
      components = value
      self._dragable_list.components = components or []
    elif is_any_list_items:
      raise ValueError("Items must be all ListItem or all stringable")
    else:
      components = self.add_drag_item(value, append=False)
  
  @property
  def order_label_visible(self):
    return self._order_label_visible
  @order_label_visible.setter
  def order_label_visible(self, value):
    self._order_label_visible = value
    self.order_label.visible = value
  
  @property
  def visible(self):
    return self._visible
  @visible.setter
  def visible(self, value):
    self._visible = value
    for comp in self.get_components():
      comp.visible = value
  
  @property
  def drag_enabled(self):
    return self._drag_enabled
  @drag_enabled.setter
  def drag_enabled(self, value):
    self._drag_enabled = value
    if getattr(self, "_dragable_list", None):
      self._dragable_list.drag_enabled = value
      
  @property
  def remove_button_properties(self):
    return self._remove_button_properties
  @remove_button_properties.setter
  def remove_button_properties(self, value):
    self._remove_button_properties = value
    if value:
      for prop, val in value.items():
        if getattr(self, "components", None) is not None:
          for comp in self.components:
            setattr(comp.remove_button, prop, val)

  @property
  def item_editable(self):
    return self._item_editable
  @item_editable.setter
  def item_editable(self, value):
    self._item_editable = value
    if getattr(self, "rendered", False):
      for comp in self.components:
        comp.editable = value

  @property
  def allow_remove(self):
    return self._allow_remove
  @allow_remove.setter
  def allow_remove(self, value):
    self._allow_remove = value
    if getattr(self, "rendered", False):
      for comp in self.components:
        comp.allow_remove = value

  def _get_list_item_value(self, comp):
    if self.numeration:
      return ". ".join(comp.item_text.split(". ")[1:])
    return comp.item_text

  def _list_changed(self, **eventargs):
    self.order_label.text = f'{self.order_title} = {self.get_ordered_comps()}'

    if self.numeration and not self.adding:
      new_comp_texts = [self._get_list_item_value(comp) for comp in self._dragable_list.get_sorted_components()]
      current_comp_texts = [self._get_list_item_value(item) for item in self.components]
      if new_comp_texts != current_comp_texts:
        self.components = [ListItem(item_text=comp_text, index=index) for index, comp_text in enumerate(new_comp_texts)]
    self.adding = False
    self.raise_event("list_changed")
    
  def get_ordered_comps(self):
    """Method to get the sorted list with each item's text"""
    return [self._get_list_item_value(comp) for comp in self._dragable_list.get_sorted_components()]
    
  def add_drag_item(self, new_texts, append=True):
    """Method to add items to the draggable list"""
    self.order_label_visible = getattr(self, "order_label_visible", True)
    self.adding = True
    if append and getattr(self, "_dragable_list", None):
      comps = self._dragable_list.get_sorted_components()
    else:
      comps = []
    if isinstance(new_texts, str):
      comps_len = len(comps)
      comps.append(ListItem(
        item_text=new_texts,
        index=comps_len,
        allow_remove=getattr(self, "allow_remove", False),
        **getattr(self, "remove_button_properties", {})
      ))
    else:
      for text in new_texts:
        comps_len = len(comps)
        comps.append(ListItem(
          item_text=text,
          index=comps_len,
          editable=getattr(self, "item_editable", False),
          **getattr(self, "remove_button_properties", {})
        ))
    self.components = comps

  def remove_drag_item(self, indices):
    """Method to remove items from the draggable list"""
    comps = self._dragable_list.get_sorted_components()
    if isinstance(indices, int):
      comps.remove(comps[indices])
    else:
      indices.sort(reverse=True)
      for index in indices:
        comps.remove(comps[index])
    self.components = comps
    
  def remove_all(self):
    self.components = []
    
  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    self.rendered = True
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
    self.components = self.components

    self.remove_button_properties = getattr(self, "remove_button_properties", None)
  
