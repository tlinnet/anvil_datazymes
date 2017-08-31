import tables
from tables import app_tables
import anvil.users
import anvil.server

# Other libraries
import bcrypt

@anvil.server.callable
def get_user_info(row):
  # Returns none, if no one is logged in
  user_row_obj = anvil.users.get_user()
  
  # If logged in:
  if user_row_obj:
    if row in ["email", "password_hash"]:
      user_info = user_row_obj[row]
    else:
      user_info = ""
    return user_info
  
@anvil.server.callable
def get_upload_log_info():
  # Returns none, if no one is logged in
  user_row_obj = anvil.users.get_user()

  # If logged in:
  if user_row_obj:
    return app_tables.upload_log.client_writable(owner=user_row_obj)

@anvil.server.callable
def get_users_db_info():
  # Returns none, if no one is logged in
  user_row_obj = anvil.users.get_user()

  # If logged in:
  if user_row_obj:
    return app_tables.users_db.client_writable(owner=user_row_obj)

@anvil.server.callable
def check_password(password):
  hashed = get_user_info("password_hash")
  if bcrypt.hashpw(password, hashed) == hashed:
    return True
  else:
    return False