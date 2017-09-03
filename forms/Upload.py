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
    self.machines_d, self.machines_l = anvil.server.call('get_machines')
    self.drop_down_machine.items = self.machines_l
    
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
        # Get info
        user = self.user
        machine = self.drop_down_machine.selected_value
        project = self.textbox_project.text

        comment = self.text_area_comment.text
        # Upload. Get OK and text
        upload_call, disp_text = anvil.server.call('file_upload', f=f, user=user, machine=machine, project=project, comment=comment)
        if not upload_call:
          Notification("Could not store: %s"%f_name,title="Files:", style="danger").show()        
          disp_text += "ERROR" + "\n"
          disp_text += "------------------" + "\n"

        # Update text field
        self.text_area_status.text += disp_text

      # When finished
      Notification("Completed processing files",title="Files:", style="success").show()
      # Clear the list of files
      self.file_loader_1.clear()
      self.Media_object_list = []