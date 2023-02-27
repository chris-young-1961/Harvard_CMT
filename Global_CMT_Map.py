#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 09:44:12 2022

@author: chrisyoung
"""

# Read in CMT catalog and plot global map of focal mechanisms

import obspy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from obspy.imaging.beachball import beach
from ReadCMT import read_cmt

# Next functiun needed because CMT catalog has format yyyy/mm/dd instead of
#  yyyy-mm-dd
def reformat_UTC_str(UTC_str):
    UTC_list = list(UTC_str)
    UTC_list[4] = '-'
    UTC_list[7] = '-'
    if UTC_list[17] == '6':
        UTC_list[17] = '0'    #C MT list sometimes has 60.0 seconds!!!
        # Should fix this to add 1 to minutes, but that may increase hours, etc.)
    UTC_str = ''.join(UTC_list)
    return UTC_str

# Event catalog information
start_str = '2010-01-01T00:00:00.0'
end_str =   '2020-01-01T00:00:00.0'
start_time = obspy.UTCDateTime(start_str)
end_time = obspy.UTCDateTime(end_str)
min_mag = 5.0
max_mag = 8.0
min_latitude = 23.
max_latitude = 48.
min_longitude = 125.
max_longitude = 150.

# Read in CMT (creates list of catalogs)
data = read_cmt('jan76_dec20.ndk')

# Create world map with colored land/ocean and coastlines
ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()

# Plot event beachballs
depth_list = [35.,70.,150.,300.,500.]
depth_color_list = [(220/255, 20/255, 60/255),  #crinmson
                    (255/255, 140/255, 0/255),  #dark orange
                    (255/255, 215/255, 0/255),  #gold
                    (0/255,128/255, 0/255),     #green
                    (0/255, 0/255, 255/255),    #blue
                    (138/255, 43/255, 226/255)] #blue violet
min_marker_size = 2.
max_marker_size = 5.
marker_scale_fac = (max_marker_size - min_marker_size)/(max_mag - min_mag)
event_count = 0
skipped_event_count = 0
for origin in data:
    UTC_str = origin['date'] + 'T' + origin['time']
    UTC_str = reformat_UTC_str(UTC_str)
    UTC_time = obspy.UTCDateTime(UTC_str)
    # Screen by mag and UTCDateTime
    if (((origin['mb'] > min_mag) | (origin['ms' ]> min_mag)) &
        (start_time <= UTC_time <= end_time)):
        # Event size scaled by magnitude
        mag = max(origin['mb'],origin['ms'])
        marker_size = min_marker_size + (mag - min_mag)*marker_scale_fac
        # Event color by depth
        depth = origin['depth']
        if depth <= depth_list[0]:
            event_color = depth_color_list[0]
        elif depth <= depth_list[1]:
            event_color = depth_color_list[1]
        elif depth <= depth_list[2]:
            event_color = depth_color_list[2]
        elif depth <= depth_list[3]:
            event_color = depth_color_list[3]
        elif depth <= depth_list[4]:
            event_color = depth_color_list[4]
        else:
            event_color = depth_color_list[5]
        mt = [origin['mrr'],origin['mtt'],origin['mpp'],origin['mrt'],
              origin['mrp'],origin['mtp']]
        # There are a few MTs in the catalog that throw an error when plotting
        # so skip those and keep a count
        try:
            b = beach(mt, xy=(origin['lon'],origin['lat']), width=marker_size, 
                      linewidth=0.2,facecolor=event_color)
            ax.add_collection(b)
            event_count += 1
        except:
            skipped_event_count+=1
        
# Add some labels at the bottom of the map
y_legend_top = -68.     # Legend labels at this latitude and below
y_inc = 6.      # Subsequent lines are this far below
textcolor = (0/255, 0/255, 0/255)  # Black
mt_strike = [0.,-1.,1.,0.,0.,0.]      # 45 degree strike slip
mt_thrust = [1.,0.,-1.,0.,0.,0.]      # dip slip, thrust
mt_normal = [-1.,0.,1.,0.,0.,0.]      # dip slip, normal
# Catalog info
x_left = -170.
ax.text(x_left, y_legend_top, 'Harvard CMT Catalog', rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, 
        fontweight = 'bold',zorder=10)
ax.text(x_left, y_legend_top - 1.*y_inc, start_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
ax.text(x_left, y_legend_top - 2.*y_inc, end_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
ax.text(x_left, y_legend_top - 3.*y_inc, str(event_count) + ' events', rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
# Foc mech types legend
x_left = -20.
ax.text(x_left, y_legend_top, 'Focal mechanism', rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, 
        fontweight = 'bold', zorder=10)
ax.text(x_left, y_legend_top - y_inc, 'strike slip fault', rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
b = beach(mt_strike, xy=(x_left-4.,y_legend_top-y_inc), width=max_marker_size, 
              linewidth=0.2,facecolor=depth_color_list[0])
ax.add_collection(b)
ax.text(x_left, y_legend_top - 2.*y_inc, 'thrust fault', rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
b = beach(mt_thrust, xy=(x_left-4.,y_legend_top-2.*y_inc), width=max_marker_size, 
              linewidth=0.2,facecolor=depth_color_list[0])
ax.add_collection(b)
ax.text(x_left, y_legend_top - 3.*y_inc, 'normal fault', rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
b = beach(mt_normal, xy=(x_left-4.,y_legend_top-3.*y_inc), width=max_marker_size, 
              linewidth=0.2,facecolor=depth_color_list[0])
ax.add_collection(b)

# Mag range legend
x_left = 150.
ax.text(x_left, y_legend_top, 'magnitude', rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, 
        fontweight = 'bold', zorder=10)
ax.text(x_left, y_legend_top - y_inc, str(max_mag), rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
b = beach(mt_strike, xy=(x_left-4.,y_legend_top-y_inc), width=max_marker_size, 
              linewidth=0.2,facecolor=depth_color_list[0])
ax.add_collection(b)
ax.text(x_left, y_legend_top - 2.*y_inc, str((min_mag+max_mag)/2.), rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
b = beach(mt_strike, xy=(x_left-4.,y_legend_top-2.*y_inc), width=(min_marker_size+max_marker_size)/2., 
              linewidth=0.2,facecolor=depth_color_list[0])
ax.add_collection(b)
ax.text(x_left, y_legend_top - 3.*y_inc, str(min_mag), rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
b = beach(mt_strike, xy=(x_left-4.,y_legend_top-3.*y_inc), width=min_marker_size, 
              linewidth=0.2,facecolor=depth_color_list[0])
ax.add_collection(b)
# Depth range legend
x_left = 50
marker_size = 0.5*(max_marker_size - min_marker_size)
ax.text(x_left, y_legend_top, 'depth [km]', rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, 
        fontweight = 'bold', zorder=10)
depth_str = '0 to ' + str(depth_list[0])
ax.text(x_left, y_legend_top - y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
b = beach(mt_strike, xy=(x_left-4.,y_legend_top-1.*y_inc), width=max_marker_size, 
              linewidth=0.2,facecolor=depth_color_list[0])
ax.add_collection(b)
depth_str = str(depth_list[0]) + ' to ' + str(depth_list[1])
ax.text(x_left, y_legend_top - 2.*y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
b = beach(mt_strike, xy=(x_left-4.,y_legend_top-2.*y_inc), width=max_marker_size, 
              linewidth=0.2,facecolor=depth_color_list[1])
ax.add_collection(b)
depth_str = str(depth_list[1]) + ' to ' + str(depth_list[2])
ax.text(x_left, y_legend_top - 3.*y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
b = beach(mt_strike, xy=(x_left-4.,y_legend_top-3.*y_inc), width=max_marker_size, 
              linewidth=0.2,facecolor=depth_color_list[2])
ax.add_collection(b)
x_left = x_left + 40.
depth_str = str(depth_list[2]) + ' to ' + str(depth_list[3])
ax.text(x_left, y_legend_top - y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
b = beach(mt_strike, xy=(x_left-4.,y_legend_top-1.*y_inc), width=max_marker_size, 
              linewidth=0.2,facecolor=depth_color_list[3])
ax.add_collection(b)
depth_str = str(depth_list[3]) + ' to ' + str(depth_list[4])
ax.text(x_left, y_legend_top - 2.*y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
b = beach(mt_strike, xy=(x_left-4.,y_legend_top-2.*y_inc), width=max_marker_size, 
              linewidth=0.2,facecolor=depth_color_list[4])
ax.add_collection(b)
depth_str = '> ' + str(depth_list[4]) 
ax.text(x_left, y_legend_top - 3.*y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
b = beach(mt_strike, xy=(x_left-4.,y_legend_top-3.*y_inc), width=max_marker_size, 
              linewidth=0.2,facecolor=depth_color_list[5])
ax.add_collection(b)

# Save the plot by calling plt.savefig() BEFORE plt.show()
plt.savefig('Global_CMT_Map.png', dpi = 300)
plt.show()
print(skipped_event_count,' events could not be plotted')