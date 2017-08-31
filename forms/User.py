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
    self.user = anvil.server.call('get_user_info', "email")
    self.label_user_email_val.text = self.user
    #self.label_user_passwdhash_val.text = anvil.server.call('get_user_info', "password_hash")
   
    # Set the dropdown
    self.dropdown_db_type_val.items = [("mysql", "mysql"), ("postgresql", "postgresql+psycopg2")]

    # Get the db_info write methods
    self.my_db_info = anvil.server.call('get_db_info')
    # Returns none, if no one is logged in. Then fill empty
    db_info_row = self.my_db_info.get(user=self.user)
    if not db_info_row:
      self.my_db_info.add_row(user=self.user,
                              db_type=self.dropdown_db_type_val.selected_value,
                              db_username="", 
                              db_password="", db_host="", 
                              db_port="", db_database="")
      # Get it again, after update
      db_info_row = self.my_db_info.get(user=self.user)
      
    # Initial update the form
    self.dropdown_db_type_val.selected_value = db_info_row['db_type']
    self.textbox_db_username_val.text = db_info_row['db_username']
    self.textbox_db_password_val.text = db_info_row['db_password']
    self.textbox_db_host_val.text = db_info_row['db_host']
    self.textbox_db_port_val.text = db_info_row['db_port']
    self.textbox_db_database_val.text = db_info_row['db_database']
    
  def button_update_click (self, **event_args):
    # This method is called when the button is clicked
    db_type = self.dropdown_db_type_val.selected_value
    db_username = self.textbox_db_username_val.text
    db_password = self.textbox_db_password_val.text
    db_host = self.textbox_db_host_val.text
    db_port = self.textbox_db_port_val.text
    db_database = self.textbox_db_database_val.text
    # Write to database. First get row, and then replace
    db_write = self.my_db_info.get(user=self.user)
    db_write["db_type"] = db_type
    db_write['db_username'] = db_username
    db_write['db_password'] = db_password
    db_write['db_host'] = db_host
    db_write['db_port'] = db_port
    db_write['db_database'] = db_database
    
    # We are done
    Notification("Update comple",title="Update:", style="success").show()