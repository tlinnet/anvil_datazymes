import tables
from tables import app_tables
import anvil.users
import anvil.server

# Other libraries
import bcrypt
import base64
import hashlib
import csv
from StringIO import StringIO
import datetime

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

@anvil.server.callable
def read_csv(in_bytes=None, delimiter=','):
  f = StringIO(in_bytes)
  reader = csv.reader(f, delimiter=delimiter, quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
  header = reader.next()
  data = [row for row in reader]
  return header, data

@anvil.server.callable
def check_csv_xy(in_bytes=None, delimiter=','):
  header, data = read_csv(in_bytes=in_bytes, delimiter=delimiter)
  if header == ['x', 'y']:
    return True
  else:
    return False

@anvil.server.callable
def file_upload(f=None, user=None, machine=None, project=None, comment=None):
  # Get the upload_log write methods
  my_upload_log_writable = get_upload_log_writable()
  disp_text = ""

  # Get the time
  date_time = datetime.datetime.now()
  disp_text += str(date_time) + "\n"
  # Get filename and content
  f_name = f.get_name()
  disp_text += f_name + "\n"
  f_content_type = f.get_content_type()
  disp_text += f_content_type + "\n"
  f_bytes = f.get_bytes()
  #disp_text += f_bytes + "\n"
  f_hashlib_md5 = get_hashlib_md5(f_bytes)

  # Upload to server
  disp_text += str(user) + "\n"
  disp_text += str(machine) + "\n"
  disp_text += str(project) + "\n"
  disp_text += str(comment) + "\n"
  disp_text += "------------------" + "\n"
  
  # Call the data base
  my_upload_log_writable.add_row(user=user, date_time=date_time, machine=machine, project=project,
                                      comment=comment, filename=f_name, md5=f_hashlib_md5)
  return True, disp_text
  
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