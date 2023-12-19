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
    self.raise_event("x-list_changed")
    
  def get_ordered_comps(self):
    """Method to get the sorted list with each item's text"""
    return [comp.text for comp in self._dragable_list.get_sorted_components()]
    
  def add_drag_item(self, new_texts):
    """Method to add items to the draggable list"""
    def generate_letter_combinations(start, count, is_lower):
        """
        Generate a sequence of letter combinations starting from the given start.
        :param start: The starting combination (e.g., 'zz').
        :param count: The number of combinations to generate.
        :param is
        :return: A list of letter combinations.
        """
        def increment_string(s):
            """
            Increment a string in a way similar to how numbers are incremented.
            'a' -> 'b', ..., 'z' -> 'aa', 'ab' -> 'ac', ..., 'zz' -> 'aaa'
            """
            if s == '':
                if is_lower:
                  return 'a'
                return "A"
            elif s[-1] == 'z':
                return increment_string(s[:-1]) + 'a'
            elif s[-1] == "Z":
                return increment_string(s[:-1]) + 'A'
            else:
                return s[:-1] + chr(ord(s[-1]) + 1)
    
        current = start
        results = []
        for _ in range(count):
            current = increment_string(current)
            results.append(current)
        if count == 1:
          return results[0]
        return results      

    comps = self._dragable_list.get_sorted_components()
    add_text = ""
    if self.numeration == "numerical":
      add_text = f"{len(comps)+1}. "
    elif self.numeration == "lower-alpha" or self.numeration == "upper-alpha":
      if not len(comps):
        add_text = f'{generate_letter_combinations("", 1, self.numeration == "lower-alpha")}. '
      else:
        add_text = f'{generate_letter_combinations(comps[-1].text.split(".")[0], 1, self.numeration == "lower-alpha")}. '
      print(add_text)
    if isinstance(new_texts, str):
      comps.append(ListItem(text=f"{add_text}{new_texts}"))
    else:
      comps += [ListItem(text=text) for text in new_texts]
    self._dragable_list.components = comps
        

  def remove_drag_item(self, index):
    """Method to remove items from the draggable list"""
    comps = self._dragable_list.get_sorted_components()
    comps.remove(comps[index])
    self._dragable_list.components = comps
    
  def remove_all(self):
    self._dragable_list.components = []
    
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


