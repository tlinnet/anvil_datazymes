from anvil import *
import anvil.server
import tables
from tables import app_tables
import anvil.users

# Python package
import datetime

class Upload (UploadTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.user = anvil.server.call('get_user_info', "email")
    self.file_loader_1.multiple = True
    self.Media_object_list = []
    # float('NaN'), to make a python nan
    self.drop_down_machine.items = ["NanoTemper", "CD", "ITC"]
    self.drop_down_project.items = ["5NT", "ITC", "TLC"]

    # Get the upload_log write methods
    self.my_upload_log_writable = anvil.server.call('get_upload_log_writable')

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
    # Enable or disable things
    self.button_upload.enabled = enabled

  def file_loader_1_change (self, files, **event_args):
    # This method is called when a new file is loaded into this FileLoader
    self.Media_object_list = files

  def button_upload_click (self, **event_args):
    # This method is called when the button is clicked
    if len(self.Media_object_list) == 0:
      Notification("There is no files added").show()
    else:
      Notification("Processing files",title="Files:", style="info").show()
      disp_text = ""
      self.text_area_status.text = disp_text
      for f in self.Media_object_list:
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
        f_hashlib_md5 = anvil.server.call('get_hashlib_md5', f_bytes)

        # Upload to server
        if True:
        #if f_content_type == "text/plain":
          # Get the formular info
          user = self.user
          disp_text += str(user) + "\n"
          machine = self.drop_down_machine.selected_value
          disp_text += str(machine) + "\n"
          project = self.drop_down_project.selected_value
          disp_text += str(project) + "\n"
          comment = self.text_area_comment.text
          disp_text += str(comment) + "\n"
          disp_text += "------------------" + "\n"
  
          # Call the data base
          self.my_upload_log_writable.add_row(user=user,
                                          date_time=date_time,
                                          machine=machine,
                                          project=project,
                                          comment=comment,
                                          filename=f_name,
                                          md5=f_hashlib_md5)
        else:
          Notification("Could not store: %s"%f_name,title="Files:", style="danger").show()        
          disp_text += "ERROR" + "\n"
          disp_text += "------------------" + "\n"

        # Update text field
        self.text_area_status.text = disp_text

      # When finished
      Notification("Completed processing files",title="Files:", style="success").show()
      # Clear the list of files
      self.file_loader_1.clear()
      self.Media_object_list = []