import os
import numpy as np
import cartopy.io.img_tiles as cimgt
from matplotlib.colors import BoundaryNorm
import matplotlib.pyplot as plt
import matplotlib
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

filename = 'C:/Users/Showlong/.local/share/cartopy/shapefiles/natural_earth/physical/10m_coastline.shp'
shape_feature = ShapelyFeature(Reader(filename).geometries(), ccrs.PlateCarree(),
                               linewidth = 1.0, facecolor = (1., 1., 1.,0.), 
                               edgecolor = 'k',zorder = 10)
fig = plt.figure(figsize = [8 , 10])
ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(shape_feature)


ax.gridlines(draw_labels=False , alpha = 0.5 , 
            xlocs = [118 , 119 , 120 , 121 , 122 , 123 , 124] , 
            ylocs = [20 , 21 , 22 , 23 , 24 , 25 , 26])

ax.set_extent([118 , 124 , 20.5 , 26.5])
ax.set_xticks([118 , 119 , 120 , 121 , 122 , 123 , 124])
ax.set_yticks([21 , 22 , 23 , 24 , 25 , 26])
ax.set_xlabel('Longitude (${^o}$)')
ax.set_ylabel('Latitude (${^o}$)')
ax.set_title('Taiwan Map')

plt.show()

fig.savefig('plotmap.png' , dpi=600)