# ---
# jupyter:
#   jupytext_format_version: '1.3'
#   jupytext_formats: py:light
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   language_info:
#     codemirror_mode:
#       name: ipython
#       version: 3
#     file_extension: .py
#     mimetype: text/x-python
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#     version: 3.7.0
# ---

# +
import numpy as np
import pandas as pd

import altair as alt

import bokeh.plotting
import bokeh.io

bokeh.io.output_notebook()
alt.data_transformers.enable('json')
# -

# ### Problem 1.2 (Beetle Hypnotists)

# a) The columns x_coord and y_coord give the coordinates of the ant's body parts in units of pixels. Create a column 'x (mm)' and a column 'y (mm)' in the data frame that has the coordinates in units of millimeters.
#
# b) Make a plot displaying the position over time of the thorax of an ant or ants placed in an area with a Dalotia beetle and position over time of an ant or ants with a Sceptobius beetle. I am intentionally not giving more specification for your plot. You need to make decisions about how to effectively extract and display the data. Think carefully about your viz. This is in many ways how you let your data speak. You could make a plot for a single ant from each genus, or for many. You will also probably need to refer to the Altair or Bokeh documentation to specify the plot as you wish.
#
# c) From this quick, exploratory analysis, what would you say about the relative activities of ants with Dalotia versus Sceptobius rove beetles?

# a) Given the x and y coordinates of the ant's body parts in units of pixels, we want to create two columns 'x (mm)' and 'y (mm)' with coordinates in millimeters. To do this, we know that the interpixel distance is 0.08 millimeters. Since the interpixel distance is equal to the length of one pixel, we can simply multiply the coordinates in pixels by the interpixel distance to get the coordinates in millimeters.

# Read in the data
df = pd.read_csv('../data/ant_joint_locations.csv', comment='#')

df.head()

# +
# Convert the coordinates from pixels to units of millimeters.

ipix = 0.08
df['x (mm)'] = df['x_coord'] * ipix
df['y (mm)'] = df['y_coord'] * ipix
df['time (ms)'] = df['frame'] / 28
# -

df.head()

# Perform some data checks
df[df['x (mm)'] < 0]

df[df['y (mm)'] < 0]

# Exclude data points where likelihood is 0.

# +
# not necessary
# df[df['likelihood'] == 0]

# +
#df1 = df[df['likelihood'] != 0]

# +
#df1.head()

# +
#df1[df1['x (mm)'] < 0]
# -

df_thorax = df[(df['bodypart'] == 'thorax')]

df_thorax.head()

# Plot with altair (attempt 2)
alt.Chart(df_thorax[df_thorax['ID'] == 1],
        height=200,
        width=200
    ).mark_point(
        size=5
    ).encode(
        x=alt.X('x (mm):Q', 
            scale=alt.Scale(domain=[0,20])
            ),
        y=alt.Y('y (mm):Q', 
            scale=alt.Scale(domain=[0,20])
            ),
        color='frame:Q',
        opacity=alt.value(0.4)
    )

# +
# Plot with altair
d = alt.Chart(df_thorax[df_thorax['ID'].isin([0,1,2,3,4,5])],
        height=120,
        width=120
    ).mark_point(
        size=2
    ).encode(
        x=alt.X('x (mm):Q', 
            scale=alt.Scale(domain=[0,20])
            ),
        y=alt.Y('y (mm):Q', 
            scale=alt.Scale(domain=[0,20])
            ),
        color='time (ms):Q',
        opacity=alt.value(0.2)
    ).facet(
        row='ID:Q'
    )

s = alt.Chart(df_thorax[df_thorax['ID'].isin([6,7,8,9,10,11])],
        height=120,
        width=120
    ).mark_point(
        size=2
    ).encode(
        x=alt.X('x (mm):Q', 
            scale=alt.Scale(domain=[0,20])
            ),
        y=alt.Y('y (mm):Q', 
            scale=alt.Scale(domain=[0,20])
            ),
        color='time (ms):Q',
        opacity=alt.value(0.2)
    ).facet(
        row='ID:Q'
    )

d | s
# -

# Plotting with Bokeh (attempt 1)

# +
p = bokeh.plotting.figure(height=450,
                          width=450)

colors = bokeh.palettes.Category20[20]
# colors
for i in range(5):
    p.line(df_thorax[df_thorax['ID'] == i]['x (mm)'], df_thorax[df_thorax['ID'] == i]['y (mm)'], color=colors[i], alpha=0.7)

# show the results
bokeh.plotting.show(p)

# +
p = bokeh.plotting.figure(height=450,
                          width=500)


colors = bokeh.palettes.Category20[20]
# colors
for i in range(5,11):
    p.line(df_thorax[df_thorax['ID'] == i]['x (mm)'], df_thorax[df_thorax['ID'] == i]['y (mm)'], color=colors[i], alpha=0.7)

# show the results
bokeh.plotting.show(p)

# +
df_thorax = df[(df['bodypart'] == 'thorax') & (df['likelihood'] != 0)]

p = bokeh.plotting.figure(height=350,
                          width=350,
                          title='Dalotia',
                          x_range=(0, 20), y_range=(0, 20))

colors = bokeh.palettes.Category20[20]
# colors
for i in range(5):
    p.line(df_thorax[df_thorax['ID'] == i]['x (mm)'], df_thorax[df_thorax['ID'] == i]['y (mm)'], color=colors[i], alpha=0.35)

p2 = bokeh.plotting.figure(height=350,
                          width=400,
                          title='Sceptobius',
                          x_range=(0, 20), y_range=(0, 20))

for i in range(5,11):
    p2.line(df_thorax[df_thorax['ID'] == i]['x (mm)'], df_thorax[df_thorax['ID'] == i]['y (mm)'], color=colors[i], alpha=0.35)

# show the results
bokeh.plotting.show(bokeh.layouts.row(p, p2))
# -

# lines are good so then you can see where they go
# it looks like there's like a problem with segmentation for some parts -- good to look at the data

# +
# create a new plot
s1 = bokeh.plotting.figure(plot_width=250, plot_height=250, title='ID = 0', x_range=(0, 20), y_range=(0, 20))
s1.line(df_thorax[df_thorax['ID'] == 0]['x (mm)'], df_thorax[df_thorax['ID'] == 0]['y (mm)'], color=colors[0], alpha=0.4)

s2 = bokeh.plotting.figure(plot_width=250, plot_height=250, title='ID = 1', x_range=(0, 20), y_range=(0, 20))
s2.line(df_thorax[df_thorax['ID'] == 1]['x (mm)'], df_thorax[df_thorax['ID'] == 1]['y (mm)'], color=colors[1], alpha=0.4)

s3 = bokeh.plotting.figure(plot_width=250, plot_height=250, title='ID = 2', x_range=(0, 20), y_range=(0, 20))
s3.line(df_thorax[df_thorax['ID'] == 2]['x (mm)'], df_thorax[df_thorax['ID'] == 2]['y (mm)'], color=colors[2], alpha=0.4)

s4 = bokeh.plotting.figure(plot_width=250, plot_height=250, title='ID = 3', x_range=(0, 20), y_range=(0, 20))
s4.line(df_thorax[df_thorax['ID'] == 3]['x (mm)'], df_thorax[df_thorax['ID'] == 3]['y (mm)'], color=colors[3], alpha=0.4)

s5 = bokeh.plotting.figure(plot_width=250, plot_height=250, title='ID = 4', x_range=(0, 20), y_range=(0, 20))
s5.line(df_thorax[df_thorax['ID'] == 4]['x (mm)'], df_thorax[df_thorax['ID'] == 4]['y (mm)'], color=colors[4], alpha=0.4)

s6 = bokeh.plotting.figure(plot_width=250, plot_height=250, title='ID = 5', x_range=(0, 20), y_range=(0, 20))
s6.line(df_thorax[df_thorax['ID'] == 5]['x (mm)'], df_thorax[df_thorax['ID'] == 5]['y (mm)'], color=colors[5], alpha=0.4)

# put the results in a row
bokeh.plotting.show(bokeh.layouts.row(s1, s2, s3, s4, s5))

# +
# create a new plot
s1 = bokeh.plotting.figure(plot_width=250, plot_height=250, title='ID = 6', x_range=(0, 20), y_range=(0, 20))
s1.line(df_thorax[df_thorax['ID'] == 6]['x (mm)'], df_thorax[df_thorax['ID'] == 6]['y (mm)'], color=colors[0], alpha=0.4)

s2 = bokeh.plotting.figure(plot_width=250, plot_height=250, title='ID = 7', x_range=(0, 20), y_range=(0, 20))
s2.line(df_thorax[df_thorax['ID'] == 7]['x (mm)'], df_thorax[df_thorax['ID'] == 7]['y (mm)'], color=colors[1], alpha=0.4)

s3 = bokeh.plotting.figure(plot_width=250, plot_height=250, title='ID = 8', x_range=(0, 20), y_range=(0, 20))
s3.line(df_thorax[df_thorax['ID'] == 8]['x (mm)'], df_thorax[df_thorax['ID'] == 8]['y (mm)'], color=colors[2], alpha=0.4)

s4 = bokeh.plotting.figure(plot_width=250, plot_height=250, title='ID = 9', x_range=(0, 20), y_range=(0, 20))
s4.line(df_thorax[df_thorax['ID'] == 9]['x (mm)'], df_thorax[df_thorax['ID'] == 9]['y (mm)'], color=colors[3], alpha=0.4)

s5 = bokeh.plotting.figure(plot_width=250, plot_height=250, title='ID = 10', x_range=(0, 20), y_range=(0, 20))
s5.line(df_thorax[df_thorax['ID'] == 10]['x (mm)'], df_thorax[df_thorax['ID'] == 10]['y (mm)'], color=colors[4], alpha=0.4)

s6 = bokeh.plotting.figure(plot_width=250, plot_height=250, title='ID = 11', x_range=(0, 20), y_range=(0, 20))
s6.line(df_thorax[df_thorax['ID'] == 11]['x (mm)'], df_thorax[df_thorax['ID'] == 11]['y (mm)'], color=colors[5], alpha=0.4)

# put the results in a row
bokeh.plotting.show(bokeh.layouts.row(s1, s2, s3, s4, s5))
# -

# The Sceptobious ant seems to stay in some specific region and not move as much as the Dalotia ants. The trace of Dalotia ants covers more of the whole arena, the position seems to be more randomly distributed across the whole arena. 

#
