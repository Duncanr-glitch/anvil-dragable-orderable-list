from ._anvil_designer import ListItemTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from anvil_extras import augment

class ListItem(ListItemTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.editable = False
    self.allow_remove = False
    
    self.item_edit_card = ColumnPanel(role="card")
    self.item_box = TextBox(role="inline-popup")
    self.item_edit_card.add_component(self.item_box)

    self.item_box.add_event_handler('pressed_enter', self.set_edited_item_text)
    self.item_box.add_event_handler('lost_focus', self.set_edited_item_text)
    augment.set_event_handler(self.item_box, "keydown", self.clear_item_changes)
    
    self.item_label.text = self.item_text
    for prop, val in properties.items():
      setattr(self.remove_button, prop, val)

  @property
  def item_text(self):
    return self._item_text
  @item_text.setter
  def item_text(self, value):
    if getattr(self, "orderable_list", None):
      numerated_text = f"{self._set_numeration_text(len(self.orderable_list.components)+1, self.orderable_list.components)}{value}"
    else:
      numerated_text = ""
    self._item_text = numerated_text
    self.item_label.text = numerated_text

  @property
  def editable(self):
    return self._editable
  @editable.setter
  def editable(self, value):
    self._editable = value
    if value:
      augment.set_event_handler(self.item_lbl_card, "dblclick", self.start_edit_item_text)
    else:
      try:
        augment.remove_event_handler(self.item_lbl_card, "dblclick", self.start_edit_item_text)
      except (ValueError, LookupError):
        print("Event doesn't exist, skipping")

  @property
  def allow_remove(self):
    return self._allow_remove
  @allow_remove.setter
  def allow_remove(self, value):
    self._allow_remove = value
    self.remove_button.visible = value

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
    
    if self.orderable_list.numeration == "numerical":
      add_text = f"{list_len}. "
    elif self.orderable_list.numeration == "lower-alpha" or self.orderable_list.numeration == "upper-alpha":
      if not list_len-1:
        add_text = f'{generate_letter_combinations("", 1, self.orderable_list.numeration == "lower-alpha")}. '
      else:
        add_text = f'{generate_letter_combinations(list_components[-1].item_text.split(".")[0], 1, self.orderable_list.numeration == "lower-alpha")}. '
    elif self.orderable_list.numeration == "lower-roman" or self.orderable_list.numeration == "upper-roman":
      add_text = f'{int_to_roman(list_len, self.orderable_list.numeration == "lower-roman")}. '
    
    return add_text

  def remove_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    confirm_remove = True
    if self.orderable_list.confirm_removal:
      confirm_remove = confirm(self.orderable_list.removal_alert_message.replace("{item_text}", "self.item_text"))

    if confirm_remove:
      self.orderable_list.remove_drag_item(self.index)

  def start_edit_item_text(self, **event_args):
    self.item_lbl_card.remove_from_parent()
    self.add_component(self.item_edit_card)
    self.item_box.focus()
    self.item_box.text = self.orderable_list._get_list_item_value(self)

  def _reset_editing_state(self, **event_args):
    self.item_edit_card.remove_from_parent()
    self.add_component(self.item_lbl_card)
    
  def set_edited_item_text(self, **event_args):
    try:
      self._reset_editing_state()
      if self.orderable_list.numeration:
        self.item_text = f"{self.item_label.text.split('. ')[0]}. {self.item_box.text}"
      else:
        self.item_text = self.item_box.text
    except ValueError:
      # This is for preventing both lost_focus and pressed_enter triggering
      pass

  def clear_item_changes(self, **event_args):
    if event_args["key"] == "Escape":
      self._reset_editing_state()
  
  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    self.orderable_list = self.parent.parent.parent.parent.parent
    self.editable = self.orderable_list.item_editable
    self.allow_remove = self.orderable_list.allow_remove
    self.it
