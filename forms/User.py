from anvil import *
import anvil.server
import tables
from tables import app_tables
import anvil.users

class User (UserTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    
    # Set the user text
    self.label_user_email.text = anvil.server.call('get_user_info', "email")
    self.label_passwd_hash.text = anvil.server.call('get_user_info', "password_hash")
   
    # Set the dropdown
    self.drop_down_db_type.items = [("mysql", "mysql"), ("postgresql", "postgresql+psycopg2")]

