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
    self._dragable_list = DragableList(drag_enabled=self.drag_enabled)
    self._dragable_list.set_event_handler(DRAGABLE_LIST_CHANGE_EVENT, self._list_changed)
    self.list_panel.add_component(self._dragable_list)
    self.adding = False
    self.rendered = False

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
    if value is not None:
      for prop, val in value.items():
        if self._dragable_list.components is not None:
          for comp in self._dragable_list.components:
            setattr(comp.remove_button, prop, val)

  @property
  def item_editable(self):
    return self._item_editable
  @item_editable.setter
  def item_editable(self, value):
    self._item_editable = value
    if getattr(self, "rendered", False):
      for comp in self._dragable_list.components:
        comp.editable = value

  @property
  def allow_remove(self):
    return self._allow_remove
  @allow_remove.setter
  def allow_remove(self, value):
    self._allow_remove = value
    if getattr(self, "rendered", False):
      for comp in self._dragable_list.components:
        comp.allow_remove = value

  def _set_numeration_text(self, list_len, list_components):
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
    def int_to_roman(num, is_lower):
        """
        Convert an integer to a Roman numeral.
        """
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
            ]
        roman_nums_upper = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
            ]
        roman_nums_lower = [
          'm', 'cm', 'd', 'cd',
          'c', 'xc', 'l', 'xl',
          'x', 'ix', 'v', 'iv',
          'i'
          ]
        roman_num = ''
        i = 0
        while num > 0:
            for _ in range(num // val[i]):
                if is_lower:
                  roman_num += roman_nums_lower[i]
                else:
                  roman_num += roman_nums_upper[i]
                num -= val[i]
            i += 1
        return roman_num

    add_text = ""
    
    if self.numeration == "numerical":
      add_text = f"{list_len}. "
    elif self.numeration == "lower-alpha" or self.numeration == "upper-alpha":
      if not list_len-1:
        add_text = f'{generate_letter_combinations("", 1, self.numeration == "lower-alpha")}. '
      else:
        add_text = f'{generate_letter_combinations(list_components[-1].item_text.split(".")[0], 1, self.numeration == "lower-alpha")}. '
    elif self.numeration == "lower-roman" or self.numeration == "upper-roman":
      add_text = f'{int_to_roman(list_len, self.numeration == "lower-roman")}. '
    
    return add_text

  def _get_list_item_value(self, comp):
    if self.numeration:
      return "".join(comp.item_text.split(". ")[1:])
    return comp.item_text

  def _list_changed(self, **eventargs):
    self.order_label.text = f'{self.order_title} = {self.get_ordered_comps()}'

    if self.numeration and not self.adding:
      comp_texts = [self._get_list_item_value(comp) for comp in self._dragable_list.get_sorted_components()]
      self._dragable_list.components = []
      self.add_drag_item(comp_texts)
    self._dragable_list.components = self._dragable_list.get_sorted_components()
    self.adding = False
    self.raise_event("list_changed")
    
  def get_ordered_comps(self):
    """Method to get the sorted list with each item's text"""
    return [self._get_list_item_value(comp) for comp in self._dragable_list.get_sorted_components()]
    
  def add_drag_item(self, new_texts):
    """Method to add items to the draggable list"""
    self.adding = True
    comps = self._dragable_list.get_sorted_components()
    if isinstance(new_texts, str):
      comps_len = len(comps)
      comps.append(ListItem(
        item_text=f"{self._set_numeration_text(comps_len+1, comps)}{new_texts}",
        index=comps_len,
        allow_remove=self.allow_remove,
        **self.remove_button_properties
      ))
    else:
      for text in new_texts:
        comps_len = len(comps)
        comps.append(ListItem(
          item_text=f"{self._set_numeration_text(comps_len+1, comps)}{text}",
          index=comps_len,
          editable=self.item_editable,
          **self.remove_button_properties
        ))
    self._dragable_list.components = comps

  def remove_drag_item(self, indices):
    """Method to remove items from the draggable list"""
    comps = self._dragable_list.get_sorted_components()
    if isinstance(indices, int):
      comps.remove(comps[indices])
    else:
      indices.sort(reverse=True)
      for index in indices:
        comps.remove(comps[index])
    self._dragable_list.components = comps
    
  def remove_all(self):
    self._dragable_list.components = []
    
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


