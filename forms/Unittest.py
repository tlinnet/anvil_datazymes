from anvil import *
import anvil.server
import tables
from tables import app_tables
import anvil.users

# unittest
import unittest
print(dir(unittest))

class Unittest (UnittestTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def button_unittest_click (self, **event_args):
    # This method is called when the button is clicked
    self.execute_unittest()

  def execute_unittest(self):
    # Execute unittests
    self.add_textarea_unittest("Hello")
    anvil.server.call('exe_unittest')
    
  def add_textarea_unittest(self, add_text):
    # Add text to the output window
    current = self.textarea_unittest.text
    current += add_text + "\n"
    self.textarea_unittest.text = current


