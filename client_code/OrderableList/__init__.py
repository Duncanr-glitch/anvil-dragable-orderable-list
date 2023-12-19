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
        add_text = f'{generate_letter_combinations(list_components[-1].text.split(".")[0], 1, self.numeration == "lower-alpha")}. '
    elif self.numeration == "lower-roman" or self.numeration == "upper-roman":
      add_text = f'{int_to_roman(list_len, self.numeration == "lower-roman")}. '
    
    return add_text

  def _list_changed(self, **eventargs):
    self.order_label.text = f'{self.order_title} = {self.get_ordered_comps()}'
    comps = self._dragable_list.get_sorted_components()
    print([comp.text for comp in comps])
    if self.numeration:
      for index, comp in enumerate(comps):
        comp.text = f'{self._set_numeration_text(index+1, comps)}{"".join(comp.text.split(". ")[1:])}'
    self.raise_event("x-list_changed")
    
  def get_ordered_comps(self):
    """Method to get the sorted list with each item's text"""
    if self.numeration:
      return ["".join(comp.text.split(". ")[1:]) for comp in self._dragable_list.get_sorted_components()]
    return [comp.text for comp in self._dragable_list.get_sorted_components()]
    
  def add_drag_item(self, new_texts):
    """Method to add items to the draggable list"""
    comps = self._dragable_list.get_sorted_components()
    if isinstance(new_texts, str):
      comps.append(ListItem(text=f"{self._set_numeration_text(len(comps)+1, comps)}{new_texts}"))
    else:
      for text in new_texts:
        comps.append(ListItem(text=f"{self._set_numeration_text(len(comps)+1, comps)}{text}"))
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


