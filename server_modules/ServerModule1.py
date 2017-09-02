import tables
from tables import app_tables
import anvil.users
import anvil.server

# Other libraries
import bcrypt
import base64
import hashlib
import csv


# Test if PRO version
try:
  import Crypto
  anvil.server.session['Crypto'] = True
except ImportError:
  anvil.server.session['Crypto'] = False
  #print("'Crypto' module is not available. Semi-safe method applied.")

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
def get_upload_log_writable():
  # Returns none, if no one is logged in
  user_row_obj = anvil.users.get_user()

  # If logged in:
  if user_row_obj:
    return app_tables.upload_log.client_writable(owner=user_row_obj)

@anvil.server.callable
def get_upload_log_readable():
  # Returns none, if no one is logged in
  user_row_obj = anvil.users.get_user()

  # If logged in:
  if user_row_obj:
    return app_tables.upload_log.client_readable(owner=user_row_obj)
  
@anvil.server.callable
def get_users_db_writable():
  # Returns none, if no one is logged in
  user_row_obj = anvil.users.get_user()

  # If logged in:
  if user_row_obj:
    return app_tables.users_db.client_writable(owner=user_row_obj)

@anvil.server.callable
def get_hashlib_md5(file_bytes):
  hashlib_calc = hashlib.md5(file_bytes).hexdigest()
  return hashlib_calc
  
@anvil.server.callable
def check_password(password):
  hashed = get_user_info("password_hash")
  if bcrypt.hashpw(password, hashed) == hashed:
    return True
  else:
    return False

# Encrypt data!
# See answer from "qneill" at: 
# https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
@anvil.server.callable
def encode(key, clear):
  enc = []
  for i in range(len(clear)):
    key_c = key[i % len(key)]
    enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
    enc.append(enc_c)
  return base64.urlsafe_b64encode("".join(enc))

@anvil.server.callable
def decode(key, enc):
  if enc == None:
    return enc

  dec = []
  enc = base64.urlsafe_b64decode(enc)
  for i in range(len(enc)):
    key_c = key[i % len(key)]
    dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
    dec.append(dec_c)
  return "".join(dec)