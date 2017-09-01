from anvil import *
import anvil.server
import tables
from tables import app_tables
import anvil.users

class Unlock (UnlockTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.correct = False
    
  #def textbox_unlock_pressed_enter (self, **event_args):
    # This method is called when the user presses Enter in this text box
  def textbox_unlock_change (self, **event_args):
    # This method is called when the text in this text box is edited
    unlock = anvil.server.call('check_password', self.textbox_unlock.text)
    # Only update if different
    checkbox_unlock_status = self.checkbox_unlock.checked
    if unlock != checkbox_unlock_status:
      self.checkbox_unlock.checked = unlock
      # Make a call to the parent class enabled function
      super(Unlock, self).enabled(self.checkbox_unlock.checked)