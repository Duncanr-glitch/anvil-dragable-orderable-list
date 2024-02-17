from ._anvil_designer import DragableListTemplate
from anvil import *
import anvil.server
from anvil.js.window import Muuri
import anvil.js

DRAGABLE_LIST_CHANGE_EVENT = 'x-dragable-list-change-event'
COMP_INDEX = 'component_index'

class DragableList(DragableListTemplate):
  """
  Modification of code found here: https://anvil.works/forum/t/cutting-edge-dragable-list-python-only/7588
  """
  def __init__(self, drag_enabled, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self._comps = None    
    self._muuri_grid = None
    self._previous_components_order = []
    self.drag_enabled = drag_enabled
    self.rendered = False

  @property
  def drag_enabled(self):
    return self._drag_enabled
  @drag_enabled.setter
  def drag_enabled(self, value):
    self._drag_enabled = value
    if getattr(self, "rendered", None):
      self._update_list()
    
  @property
  def components(self):
      return self._comps
  @components.setter
  def components(self, comps) :
      current_comps = self._comps
      try:
        if self._comps != comps:
          self._comps = comps
          if sorted([comp.item_text for comp in current_comps or []]) != sorted([comp.item_text for comp in comps or []]):
            self._update_list()
          self.raise_event(DRAGABLE_LIST_CHANGE_EVENT)
      except anvil.js.ExternalError:
        # If components are set before the dom loads fully
        pass
  
  def refresh(self):
    if self._muuri_grid:
      # self._muuri_grid.refreshItems() This does not work, for some reason.      
      # workaround:
      self.components = self.get_sorted_components()
      
  def get_sorted_components(self, **event_args) -> list:
    if self._muuri_grid is None:
      return []        
    
    return [self._comps[index] for index in self._get_components_order()]
  
  def _get_components_order(self) -> list:
    return [self._get_component_index(item) for item in self._muuri_grid.getItems()]
  
  def _get_component_index(self, item):
    return int(item.getElement().getAttribute(COMP_INDEX))
  
  def _update_list(self):
    self._init_muuri_grid()    
    for index, comp in enumerate(self._comps):
      self._muuri_grid.add(anvil.js.get_dom_node(self._generate_item(comp, index)))   
    self._previous_components_order = self._get_components_order()
      
  def _generate_item(self, component, index):
    component.remove_from_parent()
    cp = ColumnPanel(role='item')
    cp.add_component(component)
    self.dragzone.add_component(cp)
    js.get_dom_node(cp).setAttribute(COMP_INDEX, index)
    return cp
      
  def _init_muuri_grid(self):
    #Destroy old Muuri Grid    
    if self._muuri_grid != None:
      self._muuri_grid.destroy(True)
    
    self._muuri_grid = Muuri(anvil.js.get_dom_node(self.dragzone),{
    'dragEnabled': self.drag_enabled,
    'items': None,
    'dragAxis': 'y',
    'fillGaps': False,
    'dragAutoScroll': self._get_drag_settings()
    })
    self._muuri_grid.on('dragEnd', self._drag_end)
    self.dragzone.clear()
    
  def _drag_end(self, item, event):
    current_components_order = self._get_components_order()
    if current_components_order != self._previous_components_order:
      self._previous_components_order = current_components_order
      self.raise_event(DRAGABLE_LIST_CHANGE_EVENT)

  def _get_drag_settings(self):
      return {
      'targets': [
        # Scroll window on both x-axis and y-axis.
        { 'element': anvil.js.get_dom_node(self.dragzone), 'priority': 0, 'axis': Muuri.AutoScroller.AXIS_Y },
        # Scroll scrollElement (can be any scrollable element) on y-axis only,
        # and prefer it over window in conflict scenarios.
        #{ 'element': scrollElement, 'priority': 1, 'axis': Muuri.AutoScroller.AXIS_Y },
      ],
      # Let's use the dragged item element as the handle.
      'handle': None,
      # Start auto-scroll when the distance from scroll target's edge to dragged
      # item is 40px or less.
      'threshold': 60,
      # Make sure the inner 10% of the scroll target's area is always "safe zone"
      # which does not trigger auto-scroll.
      'safeZone': 0.1,
      # Let's define smooth dynamic speed.
      # Max speed: 2000 pixels per second
      # Acceleration: 2700 pixels per second
      # Deceleration: 3200 pixels per second.
      'speed': Muuri.AutoScroller.smoothSpeed(1000, 1500, 2000),
      # Let's not sort during scroll.
      'sortDuringScroll': False,
      # Enable smooth stop.
      'smoothStop': True,
      }

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    self.rendered = True
