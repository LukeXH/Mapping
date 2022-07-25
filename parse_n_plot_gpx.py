from turtle import position
import gpxpy
import gpxpy.gpx

import matplotlib.pyplot as plt

import pymap3d as pm

# Parsing an existing file:
# -------------------------

gpx_file = open('data/20220720-124753 - Hotlap plus lunch.gpx', 'r')

gpx = gpxpy.parse(gpx_file)

lat_list = []
lon_list = []
enu_origin = gpxpy.gpx.GPXTrackPoint()
enu = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            # Set the enu_origin as start
            if not enu_origin.latitude and not enu_origin.longitude and not enu_origin.elevation:
                enu_origin.latitude = point.latitude
                enu_origin.longitude = point.longitude
                enu_origin.elevation = point.elevation
            # print(f'Point at ({enu_origin.latitude},{enu_origin.longitude}) -> {enu_origin.elevation}')
            lat_list.append(point.latitude)
            lon_list.append(point.longitude)
            enu.append(pm.geodetic2enu( point.latitude, 
                                        point.longitude, 
                                        point.elevation, 
                                        enu_origin.latitude, 
                                        enu_origin.longitude, 
                                        enu_origin.elevation))

for waypoint in gpx.waypoints:
    print(f'waypoint {waypoint.name} -> ({waypoint.latitude},{waypoint.longitude})')

# Plotting the file:
# -------------------------
# Create four polar axes and access them through the returned array
fig, axs = plt.subplots(1, 2)
axs[0].plot(lon_list, lat_list)
axs[0].plot([enu_origin.longitude], [enu_origin.latitude], 'ro', markersize=5)
axs[0].axis('equal')
axs[1].plot([p[0] for p in enu], [p[1] for p in enu])
axs[1].plot([0],[0], 'ro', markersize=5)
axs[1].axis('equal')
# plt.plot(lon_list, lat_list)
# plt.ylabel('Lat')
# plt.xlabel('Lon')
plt.show()