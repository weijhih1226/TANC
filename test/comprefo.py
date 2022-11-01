import os
import numpy as np
from matplotlib.colors import BoundaryNorm
import matplotlib.pyplot as plt
import matplotlib
from reader.radar_read import read_compref

fname = 'CREF.20200811.065000'
cref = read_compref(fname)

dbz = cref.var.reshape(cref.ny,cref.nx)/float(cref.var_scale)
max_lat = cref.alat/cref.map_scale
max_lon = (cref.alon/cref.map_scale) + cref.nx*(cref.dx/cref.dxy_scale )
min_lat = (cref.alat/cref.xy_scale)-cref.ny*(cref.dy/cref.dxy_scale) 
min_lon = cref.alon/cref.map_scale
print('max_lat = ',max_lat)
print('max_lon = ',max_lon)
print('min_lat = ',min_lat)
print('min_lon = ',min_lon)
print('radars  = ',cref.radars)
for i in range(len(dbz)):
    for j in range(len(dbz[0])):
        if dbz[i][j] == -999.0 or dbz[i][j] == -99.0:
            dbz[i][j] = np.nan

colorss = [#'#FFFFFF',
          '#635273',
          '#736384',
          '#9c9c9c',
          '#00ce00',
          '#00ad00',
          '#009400',
          '#ffff00',
          '#e7c600',
          '#ff9400',
          '#ff6363',
          '#ff0000',
          '#ce0000',
          '#ff00ff',
          '#9c31ce',
          '#ffffff'
          ]
radar_cm = matplotlib.colors.ListedColormap(colorss)
#radar_cm.set_bad('#122730', 0.10)
cLevel = [-990]+[i for i in range(10,85,5)]
fig, ax = plt.subplots(figsize=(57.60,62.40))#,subplot_kw={'projection':ccrs.PlateCarree()})
norm = BoundaryNorm(cLevel, ncolors=radar_cm.N, clip=True)

cn = ax.pcolormesh(dbz,cmap=radar_cm, norm=norm)

axpos = ax.get_position()
pos_x = axpos.x0+axpos.width - 0.05# + 0.25*axpos.width
pos_y = axpos.y0+0.01
cax_width = 0.022
cax_height = (axpos.height)/3
pos_cax = fig.add_axes([pos_x,pos_y,cax_width,cax_height])
cbar = plt.colorbar(cn, cax=pos_cax)
cbar.ax.tick_params(labelsize=45,colors = 'black') 
#ax.set_aspect('auto', adjustable=None)
#ax.set_title('COMPREF_202007230820', fontsize=60)

if len(str(cref.hh)) < 2:
    hh = '0'+str(cref.hh)
else:
    hh = str(cref.hh)

if len(str(cref.mn)) < 2:
    mn = '0'+str(cref.mn)
else:
    mn = str(cref.mn)

name2 = fname.split('.')[0]+str(cref.yyyy)+str(cref.mm)+str(cref.dd)+hh+mn

plt.savefig(name2+'.png')

