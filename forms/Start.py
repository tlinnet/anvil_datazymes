from anvil import *
import anvil.server
import tables
from tables import app_tables
import anvil.users
from User import User
from Upload import Upload
from Dash_upload import Dash_upload
from About import About
from Page_unittest import Page_unittest

class Start (StartTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)
    
    # Start login. Returns None, if they press cancel.
    # We keep the login screen, as long as they have not logged in

    # Login
    anvil.users.login_with_email("test@test.test","test")
    #while not anvil.users.login_with_form():
    #  pass

    # Perform unittest after login
    #import test_me
    
    #### Any code you write here will run when the form opens.
    # Reset home page
    self.link_upload_click()

  def link_upload_click (self, **event_args):
    # This method is called when the link is clicked
    self.content_panel.clear()
    self.content_panel.add_component(Upload())
    
  def link_user_click (self, **event_args):
    # This method is called when the link is clicked
    self.content_panel.clear()
    self.content_panel.add_component(User())

  def link_dash_upload_click (self, **event_args):
    # This method is called when the link is clicked
    self.content_panel.clear()
    self.content_panel.add_component(Dash_upload())

  def link_about_click (self, **event_args):
    # This method is called when the link is clicked
    self.content_panel.clear()
    self.content_panel.add_component(About())

  def link_unittest_click (self, **event_args):
    # This method is called when the link is clicked
    self.content_panel.clear()
    self.content_panel.add_component(Page_unittest())



