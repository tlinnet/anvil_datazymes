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
    self.label_user_email_val.text = anvil.server.call('get_user_info', "email")
    self.label_user_passwdhash_val.text = anvil.server.call('get_user_info', "password_hash")
   
    # Set the dropdown
    self.dropdown_db_type_val.items = [("mysql", "mysql"), ("postgresql", "postgresql+psycopg2")]

    # Get the db_info
    self.my_db_info = anvil.server.call('get_db_info')

    # Get the row
    for row in self.my_db_info.search():
      print(row)

  def button_update_click (self, **event_args):
    # This method is called when the button is clicked
    print("db_type:", self.dropdown_db_type_val.selected_value)
#    print("db_username:" self.textbox_)
    self.textbox_db_username_val.
