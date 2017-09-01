from anvil import *
import anvil.server
import tables
from tables import app_tables
import anvil.users
#from Unlock import Unlock

class User (UserTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    
    # Set the user text
    self.user = anvil.server.call('get_user_info', "email")
    self.label_user_email_val.text = self.user
    #self.label_user_passwdhash_val.text = anvil.server.call('get_user_info', "password_hash")
    
    # NOT implemented yet! 
    # Load the Unlock into the linear unlock panel. Add Unlock, by instante
    #self.linear_unlock.clear()
    #unlock = Unlock()
    #self.linear_unlock.add_component(unlock)
    
    # Set the dropdown
    #self.dropdown_db_type_val.items = [("postgresql", "postgresql+psycopg2"), ("mysql", "mysql")]
    self.dropdown_db_type_val.items = [("postgresql", "postgresql+psycopg2")]
    
    # Get the db_info write methods
    self.my_users_db_writable = anvil.server.call('get_users_db_writable')
    # Returns none, if no one is logged in. Then fill empty
    db_info_row = self.my_users_db_writable.get(user=self.user)
    if not db_info_row:
      self.my_users_db_writable.add_row(user=self.user)

    # Initial update the form not to be enabled
    self.enable_change(enabled=False)

  #def textbox_unlock_pressed_enter (self, **event_args):
    # This method is called when the user presses Enter in this text box
  def textbox_unlock_change (self, **event_args):
    # This method is called when the text in this text box is edited
    unlock = anvil.server.call('check_password', self.textbox_unlock.text)
    # Only update if different
    checkbox_unlock_status = self.checkbox_unlock.checked
    if unlock != checkbox_unlock_status:
      self.checkbox_unlock.checked = unlock
      # Make a call to the unlock change
      self.enable_change(enabled=self.checkbox_unlock.checked)

  def enable_change(self, enabled):
    # Enable or disable the boxes
    self.dropdown_db_type_val.enabled = enabled
    self.textbox_db_username_val.enabled = enabled
    self.textbox_db_password_val.enabled = enabled
    self.textbox_db_host_val.enabled = enabled
    self.textbox_db_port_val.enabled = enabled
    self.textbox_db_database_val.enabled = enabled
    self.button_update.enabled = enabled
    # Define values if enabled
    if enabled:
      # Get info
      db_info_row = self.my_users_db_writable.get(user=self.user)
      db_type = anvil.server.call('decode', self.textbox_unlock.text, db_info_row['db_type'])
      db_username = anvil.server.call('decode', self.textbox_unlock.text, db_info_row['db_username'])
      db_password = anvil.server.call('decode', self.textbox_unlock.text, db_info_row['db_password'])
      db_host = anvil.server.call('decode', self.textbox_unlock.text, db_info_row['db_host'])
      db_port = anvil.server.call('decode', self.textbox_unlock.text, db_info_row['db_port'])
      db_database = anvil.server.call('decode', self.textbox_unlock.text, db_info_row['db_database'])
    else:
      db_type = self.dropdown_db_type_val.selected_value
      db_username = ""
      db_password = ""
      db_host = ""
      db_port = ""
      db_database = ""

    # Fill data
    #self.dropdown_db_type_val.selected_value = db_type
    self.set_dropdown_selected_value(self.dropdown_db_type_val, db_type)
    self.textbox_db_username_val.text = db_username
    self.textbox_db_password_val.text = db_password
    self.textbox_db_host_val.text = db_host
    self.textbox_db_port_val.text = db_port
    self.textbox_db_database_val.text = db_database

  def set_dropdown_selected_value(self, dropmod, new_item):
    # Make sure that drop down filling is safe
    dropmod_items = getattr(dropmod, 'items')
    dropmod_selected_value = getattr(dropmod, 'selected_value')
    if new_item not in dropmod_items:
      dropmod_selected_value = dropmod_items[0]

  def button_update_click (self, **event_args):
    # This method is called when the button is clicked
    # First get the values
    db_type = self.dropdown_db_type_val.selected_value
    db_username = self.textbox_db_username_val.text
    db_password = self.textbox_db_password_val.text
    db_host = self.textbox_db_host_val.text
    db_port = self.textbox_db_port_val.text
    db_database = self.textbox_db_database_val.text
    # Write to database. First get row, and then replace
    db_write = self.my_users_db_writable.get(user=self.user)
    db_write["db_type"] = anvil.server.call('encode', self.textbox_unlock.text, db_type)
    db_write['db_username'] = anvil.server.call('encode', self.textbox_unlock.text, db_username)
    db_write['db_password'] = anvil.server.call('encode', self.textbox_unlock.text, db_password)
    db_write['db_host'] = anvil.server.call('encode', self.textbox_unlock.text, db_host)
    db_write['db_port'] = anvil.server.call('encode', self.textbox_unlock.text, db_port)
    db_write['db_database'] = anvil.server.call('encode', self.textbox_unlock.text, db_database)
    
    # We are done
    Notification("Update complete",title="Update:", style="success").show()
