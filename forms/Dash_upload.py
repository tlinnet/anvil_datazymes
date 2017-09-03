from anvil import *
import anvil.server
import tables
from tables import app_tables
import anvil.users

# Other
from collections import Counter
from plotly import graph_objs as go

class Dash_upload (Dash_uploadTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
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
    self.plot_1.data = [scatter]
    
    # Get projects
    projects = anvil.server.call('list_xy_csv_get_projects')
    self.dropdown_projects.items = [('All', None)] + projects

  def dropdown_projects_change (self, **event_args):
    # This method is called when an item is selected
    datasets = anvil.server.call('list_xy_csv_get_p_datasets', project=self.dropdown_projects.selected_value)
    # Make out
    items = []
    for dataset in datasets:
      items.append(dataset[0]+dataset[1])
    self.dropdown_project_sets.items = items
    
  def dropdown_project_sets_change (self, **event_args):
    # This method is called when an item is selected
    print(dropdown_project_sets.selected_value)


