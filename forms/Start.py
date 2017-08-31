from anvil import *
import anvil.server
import tables
from tables import app_tables
import anvil.users
from User import User
from Home import Home

class Start (StartTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)
    
    # Start login. Returns None, if they press cancel.
    # We keep the login screen, as long as they have not logged in
    while not anvil.users.login_with_form():
      pass
    #### Any code you write here will run when the form opens.
    # Reset home page
    self.link_home_click()

  def link_home_click (self, **event_args):
    # This method is called when the link is clicked
    self.content_panel.clear()
    self.content_panel.add_component(Home())
    
  def link_user_click (self, **event_args):
    # This method is called when the link is clicked
    self.content_panel.clear()
    self.content_panel.add_component(User())

