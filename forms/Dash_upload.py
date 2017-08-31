from anvil import *
import anvil.server
import tables
from tables import app_tables
import anvil.users

# Other
from plotly import graph_objs as go

class Dash_upload (Dash_uploadTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    x = [3.4, 4.5, 5.6, 6.7, 8.9]
    y = [4.4, 5.5, 6.6, 7.7, 9.9]

    # Get the upload_log read methods
    self.my_upload_log_readable = anvil.server.call('get_upload_log_readable')

    # Collect
    x_times = []
    for row in self.my_upload_log_readable.search():
      x_times.append(row["machine"])

    scatter = go.Scatter(x = x, y = y, fill='tozeroy')
    self.plot_1.data = [scatter]