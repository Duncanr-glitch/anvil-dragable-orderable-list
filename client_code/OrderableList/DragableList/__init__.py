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
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.components = None    
    self._muuri_grid = None
    self._previous_components_order = []
    self._drag_enabled = True
    
  @property
  def _drag_enabled(self):
    return self.__drag_enabled
  @_drag_enabled.setter
  def _drag_enabled(self, value):
    self.__drag_enabled = value
    try:
      self._update_list()
    except Exception as err:
      # if str(err) == "Error: Container element must be an existing DOM element.":
      #   # Just for the first time around when the dom isn't ready
      #   pass
      # else:
      #   raise
      pass
  
  @property
  def components(self):
    return self._components

  @components.setter
  def components(self, comps):
    self._components = comps
    # if getattr(self, "_components", None) != comps:
      # self._comps = comps
    print(getattr(self, "_muuri_grid", None))
    try:
      self._update_list()
      self.raise_event(DRAGABLE_LIST_CHANGE_EVENT)
    except:
      # if str(err) == "Error: Container element must be an existing DOM element.":
      #   # Just for the first time around when the dom isn't ready
      #   pass
      # else:
      #   raise
      pass
  
  def refresh(self):
    if self._muuri_grid:
      # self._muuri_grid.refreshItems() This does not work, for some reason.      
      # workaround:
      self.components = self.get_sorted_components()
      
  def get_sorted_components(self, **event_args) -> list:
    if self._muuri_grid is None:
      return []        
    
    return [self.components[index] for index in self._get_components_order()]
  
  def _get_components_order(self) -> list:
    return [self._get_component_index(item) for item in self._muuri_grid.getItems()]
  
  def _get_component_index(self, item):
    return int(item.getElement().getAttribute(COMP_INDEX))
  
  def _update_list(self):
    self._init_muuri_grid()    
    for index, comp in enumerate(self.components):
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
    if getattr(self, "_muuri_grid", None) != None:
      self._muuri_grid.destroy(True)
    print("here")
    self._muuri_grid = Muuri(anvil.js.get_dom_node(self.dragzone),{
    'dragEnabled': getattr(self, "_drag_enabled", True),
    'items': None,
    'dragAxis': 'y',
    'fillGaps': False,
    'dragAutoScroll': self._get_drag_settings()})
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