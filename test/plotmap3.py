import netCDF4 as nc
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

# fig , ax = plt.subplots(figsize=(8 , 6) , subplot_kw={'projection' : ccrs.PlateCarree()})
# ax.set_extent([118 , 124 , 20 , 26])
# ax.coastlines(resolution = '10m')
# plt.show()

shp_filename = 'C:/Users/Showlong/.local/share/cartopy/shapefiles/natural_earth/physical/10m_coastline.shp'
shape_feature = ShapelyFeature(Reader(shp_filename).geometries(), ccrs.PlateCarree(),
                               linewidth = 1.0, facecolor = (1., 1., 1.,0.), 
                               edgecolor = 'w',zorder = 10)

# Set Path
dir = "C:/Users/Showlong/Desktop/PythonTest/20200801/"
file = "20200801_153000.nc"
path = dir + file

datagrp = nc.Dataset(path)
datagrp

# Variables
time = datagrp.variables['time'][:]
x0 = datagrp.variables['x0'][:]
y0 = datagrp.variables['y0'][:]
z0 = datagrp.variables['z0'][:]
Temp_Rate = datagrp.variables['Temp_Rate'][:]
Temp_Rate = Temp_Rate.reshape(500 , 400)
xx , yy = np.meshgrid(x0 , y0)

# Set Colormap
color_roc = [
          '#00008b',
          '#0000cd',
          '#6495ed',
          '#00ffff',
          '#006400',
          '#3cb371',
          '#00ff7f',
          '#f5deb3',
          '#b8860b',
          '#ffd700',
          ]
cm_roc = ListedColormap(color_roc)

# Plot
lvls = [-40, -24, -20, -16, -12, -8, -4, -2, 2, 8, 20]
norm = BoundaryNorm(lvls , cm_roc.N)

# matplotlib.use('TkAgg')

plt.style.use(['dark_background'])
fig , ax = plt.subplots(figsize = [6.4 , 4.8] , subplot_kw={'projection':ccrs.PlateCarree()})
ax.add_feature(shape_feature)
ax.gridlines(draw_labels=False , alpha = 0.5 , 
            xlocs = [118 , 119 , 120 , 121 , 122 , 123 , 124] , 
            ylocs = [20 , 21 , 22 , 23 , 24 , 25 , 26])
ax.set_extent([119 , 123 , 21 , 26])
ax.set_xticks([119 , 120 , 121 , 122 , 123])
ax.set_yticks([21 , 22 , 23 , 24 , 25 , 26])

CS = ax.contourf(xx , yy , Temp_Rate , levels = lvls , cmap = cm_roc , norm = norm , alpha = 1)
CS.set_clim(-40 , 20)
ax.set_xlabel('Longitude (${^o}$)')
ax.set_ylabel('Latitude (${^o}$)')
plt.title('TANC - Rate of Change')
cbar = plt.colorbar(CS , orientation = 'vertical', ticks = lvls)
cbar.set_label('${^o}$C/15min')
plt.show()
fig.savefig('plot.png' , dpi = 200)