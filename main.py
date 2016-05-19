def histogram_plot(states, height, width, data_top, data_source, n_ticks,
        n_minor_ticks=0, fill_color=None):
    '''Create a bokeh histogram using quad shapes'''
    from bokeh.plotting import Figure

    # Create histogram object
    hist_obj = Figure(plot_height=height, plot_width=width, title="",
                      toolbar_location=None)

    # Data top is string of var name from data_source
    fill_color = '#f0f5f5' if fill_color==None else fill_color
    hist_obj.quad(top=data_top, bottom=0, source=data_source, left="left",
                  right="right", fill_color=fill_color, line_color='black')

    # set number of major and minor ticks
    hist_obj.xaxis[0].ticker.desired_num_ticks = n_ticks
    hist_obj.xaxis[0].ticker.num_minor_ticks = n_minor_ticks

    hist_obj.y_range = Range1d(0, 1)
    hist_obj.x_range = Range1d(states[0]-0.5, states[-1]+0.5)

    return hist_obj


def landscape_plot(landscape, states, timesteps, height, width, patch_colors):
    '''Plot fitness landscape'''
    from bokeh.plotting import Figure

    # Append extra state and timestep for index bounds of quad objects
    states = numpy.append(states, states[-1]+1)
    timesteps = numpy.append(timesteps, timesteps[-1]+1)

    # Create points for each cell of grid
    tops = list()
    bottoms = list()
    lefts = list()
    rights = list()
    for top, bottom in zip(states[1:], states[:-1]):
        for left, right in zip(timesteps[:-1], timesteps[1:]):
            tops.append(top)
            bottoms.append(bottom)
            lefts.append(left)
            rights.append(right)

    # Create array of color values corresponding to each cell's assoc. patch
    grid_colors = list()
    for i in range(len(tops)):
        idx = (landscape['state']==bottoms[i]) & (landscape['t']==lefts[i])
        patch = int(landscape[idx]['patch'])
        grid_colors.append(patch_colors[patch])

    # Create landscape object
    grid_obj = Figure(plot_height=height, plot_width=width, title="", toolbar_location=None)
    grid_obj.quad(top=tops, bottom=bottoms, left=lefts, right=rights, line_color='black',
            fill_color=grid_colors)

    return grid_obj


def select_data():
    '''Get data selection from plot controls'''

    data = locations[(locations['t'] == slide_time.value) &
                     (locations['state'] >= slide_state_min.value) &
                     (locations['state'] <= slide_state_max.value)]
    return data


def update(attrname, old, new):
    '''Update plots from selected data'''

    data_selected = select_data()

    idx_dead = (data_selected['alive']==0)
    idx_p0 = (data_selected['patch']==0) & (data_selected['alive']==1)
    idx_p1 = (data_selected['patch']==1) & (data_selected['alive']==1)
    idx_p2 = (data_selected['patch']==2) & (data_selected['alive']==1)

    # Total histogram
    ht.xaxis.axis_label = x_axis.value
    ht.yaxis.axis_label = y_axis.value
    ht.title = "All patches: %d organisms" % len(data_selected)

    # Dead histogram
    hd.xaxis.axis_label = x_axis.value
    hd.yaxis.axis_label = y_axis.value
    hd.title = "Dead: %d organisms" % len(data_selected[idx_dead])

    # Patch 0 histogram
    h0.xaxis.axis_label = x_axis.value
    h0.yaxis.axis_label = y_axis.value
    h0.title = "Patch 0: %d organisms" % len(data_selected[idx_p0])

    # Patch 1 histogram
    h1.xaxis.axis_label = x_axis.value
    h1.yaxis.axis_label = y_axis.value
    h1.title = "Patch 1: %d organisms" % len(data_selected[idx_p1])

    # Patch 2 histogram
    h2.xaxis.axis_label = x_axis.value
    h2.yaxis.axis_label = y_axis.value
    h2.title = "Patch 2: %d organisms" % len(data_selected[idx_p2])

    states = numpy.unique(data_selected['state'])
    bins = len(states)

    hist_t, _   = numpy.histogram(data_selected['state'], density=True,
                                  bins=bins)
    hist_d, _   = numpy.histogram(data_selected['state'][idx_dead], density=True,
                                  bins=bins)
    hist_p0, _  = numpy.histogram(data_selected['state'][idx_p0], density=True,
                                  bins=bins)
    hist_p1, _  = numpy.histogram(data_selected['state'][idx_p1], density=True,
                                  bins=bins)
    hist_p2, _  = numpy.histogram(data_selected['state'][idx_p2], density=True,
                                  bins=bins)
    edges = [i for i in numpy.arange(min(states)-0.5, max(states)+1, 1)]

    source.data = dict(
        x = list(data_selected['t']),
        timestep = list(data_selected['t']),
        state = list(data_selected['state']),
        hist_t = hist_t,
        hist_d = hist_d,
        hist_p0 = hist_p0,
        hist_p1 = hist_p1,
        hist_p2 = hist_p2,
        left  = edges[:-1],
        right = edges[1:],
        )

    return None


from os.path import dirname, join

import numpy
from bokeh.models import ColumnDataSource, HoverTool, HBox, VBoxForm
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.models.ranges import Range1d
from bokeh.io import curdoc

# Setup data
landscape = numpy.load('./landscape.npy')
locations = numpy.load('./locations.npy')

patch_colors = {0:'#005F6B', 1:'#00B4CC', 2:'#00DFFC'}

t_min = numpy.min(locations['t'])
t_max = numpy.max(locations['t'])

timesteps = numpy.unique(locations['t'])
states = numpy.unique(locations['state'])
bins = len(states)

state_min = numpy.min(states)
state_max = numpy.max(states)

axis_map = {
            "Time": "t",
            "State": "state",
            "% of Individuals": "percent",
           }

# Create Input controls
slide_time = Slider(title="Time-step", start=t_min, end=t_max, value=t_min,
                    step=1)

slide_state_min = Slider(title="Minimum state", start=state_min, end=state_max,
                         value=state_min, step=1)
slide_state_max = Slider(title="Maximum state", start=state_min, end=state_max,
                         value=state_max, step=1)

x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value='State')
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()),
                                               value='% of Individuals')

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], timestep=[], state=[]))

#TODO remove when not needed
#hover = HoverTool(tooltips=[
#    ("X acc.","@timestep"),
#    ("Year", "@year"),
#    ("$", "@revenue")
#])

# Histogram of all patches, patch 0, patch1, and patch 2
ht = histogram_plot(states, 400, 400, 'hist_t', source, bins, n_minor_ticks=0,
                    fill_color=None)
hd = histogram_plot(states, 400, 400, 'hist_d', source, bins, n_minor_ticks=0,
                    fill_color="red")
h0 = histogram_plot(states, 400, 400, 'hist_p0', source, bins, n_minor_ticks=0,
                    fill_color = patch_colors[0])
h1 = histogram_plot(states, 400, 400, 'hist_p1', source, bins, n_minor_ticks=0,
                    fill_color = patch_colors[1])
h2 = histogram_plot(states, 400, 400, 'hist_p2', source, bins, n_minor_ticks=0,
                    fill_color = patch_colors[2])

# Landscape plot
grid = landscape_plot(landscape, states, timesteps, 400, 800, patch_colors)
grid.title = 'Patch selection landscape'

#TODO remove when not needed
#s2.circle(x="x", y="state", source=source, size=7, color="#EB6841",
#line_color=None, fill_alpha=0.9)


controls = [slide_time, slide_state_min, slide_state_max]#, x_axis, y_axis]
for control in controls:
    control.on_change('value', update)

inputs = HBox(VBoxForm(*controls), width=300)

# initial load of the data
update(None, None, None)

curdoc().add_root(HBox(ht, grid, inputs, width=1100))
curdoc().add_root(HBox(h0, h1, h2, hd, width=1100))
