from anvil import *
import anvil.server
import tables
from tables import app_tables
import anvil.users

import sys

class About (AboutTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def button_unittest_click (self, **event_args):
    # This method is called when the button is clicked
    import test_me
    print("Completed")
    Notification("Unittests complete",title="Unittesting:", style="info").show()

