from anvil import *
import anvil.server
import tables
from tables import app_tables
import anvil.users

# Other
from collections import Counter
from plotly import graph_objs as go
import datetime

class Dash_upload (Dash_uploadTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Plot the uploads
    self.plot_upload_func()
    
    # Get projects and fill them:
    projects = anvil.server.call('list_xy_csv_get_projects')
    # Fill the projects
    self.dropdown_projects.items = [('All', None)] + projects
    # Fill the data
    self.dropdown_projects_change()
    
  def plot_upload_func(self):
    # Get the upload_log read methods
    self.my_upload_log_readable = anvil.server.call('get_upload_log_readable')

    # Collect
    x_times = []
    for row in self.my_upload_log_readable.search():
      x_times.append( str(row['date_time'].date()) )

    # Make a counter
    x_times_c = Counter(x_times)
    # Sort it
    x_times_c_s = sorted(x_times_c.items())
    # Unzip from 2-tubles in list
    if len(x_times_c_s) == 0:
      x_times_c_s = [('0', 0)]
    x_plot, y_plot = zip(*x_times_c_s)

    # Plot
    scatter = go.Scatter(x = x_plot, y = y_plot, fill='tozeroy')
    self.plot_upload.data = [scatter]

  def dropdown_projects_change (self, **event_args):
    # This method is called when an item is selected
    datasets = anvil.server.call('list_xy_csv_get_p_datasets', project=self.dropdown_projects.selected_value)
    # Make out
    items = []    
    for i, dataset in enumerate(datasets):
      # Extract dataa
      md5, user, date_time, machine, project, comment, filename = dataset
      # Convert datatime to string
      date_time_str = date_time.strftime("%Y-%m-%d %H:%M:%S")
      # Add to dropdown list
      items.append(("%s ; %s ; %s"%(date_time_str, machine, comment), "%s"%md5))
      if i == 0:
        self.set_textarea_project_set(md5=md5, user=user, date_time=date_time, machine=machine, project=project, comment=comment, filename=filename)

    # Set dataset items for project
    self.dropdown_project_sets.items = items
    # Call the first change
    self.dropdown_project_sets_change()

  def set_textarea_project_set(self, md5="", user="", date_time=datetime.datetime.now(), machine="", project="", comment="", filename=""):
    # Make empty
    disp_text = ""
    self.textarea_project_sets.text = ""
    # Convert datatime to string
    if md5:
      date_time_str = date_time.strftime("%Y-%m-%d %H:%M:%S")
      # Add to text out
      disp_text += "date_time: %s" % date_time_str + "\n"
      disp_text += "project: %s" % project + "\n"
      disp_text += "machine: %s" % machine + "\n"
      disp_text += "filename: %s" % filename + "\n"
      disp_text += "comment: %s" % comment + "\n"
      # Set text
      self.textarea_project_sets.text = disp_text

  def dropdown_project_sets_change (self, **event_args):
    # This method is called when an item is selected
    md5 = self.dropdown_project_sets.selected_value
    x_l, y_l, info = anvil.server.call('list_xy_csv_get_xy', md5=md5) 
    # Extract info
    md5, user, date_time, machine, project, comment, filename = info
    # Write info
    self.set_textarea_project_set(md5=md5, user=user, date_time=date_time, machine=machine, project=project, comment=comment, filename=filename)
    # Make plot
    self.plot_xy_func(x_l, y_l)
    
  def plot_xy_func(self, x=None, y=None):
    # Sort data
    if (x and y):
      x, y = zip(*sorted(zip(x, y)))
    else:
      x, y = 0, 0
    # Plot
    scatter = go.Scatter(x = x, y = y)
    self.plot_xy.data = [scatter]
