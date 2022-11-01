#===================================================
#使用cartopy繪製地圖
#需要從http://www.naturalearthdata.com/downloads/下載shape檔案
#下載後，解壓縮，檔名統一去掉"ne_"開頭，拷貝至D:\Program Files\
#WinPython-32bit-2.7.9.3\settings\.local\share\cartopy\shapefiles\natural_earth\physical\
#路徑下面，coastline檔案對應ax.coastlines命令，land檔案對應land命令
#===================================================

scale='110m'
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
#exit(0)
fig=plt.figure(figsize=(8, 10))
ax=plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
ax.set_global()

#===================================================
#需要填充陸地顏色時使用
#ax.add_feature(cfeature.LAND, facecolor='0.75') #預設為110m，其它解析度需用下面命令
land = cfeature.NaturalEarthFeature('physical', 'land', scale,edgecolor='face',
                                                              facecolor=cfeature.COLORS['land'])
ax.add_feature(land, facecolor='0.75')
#===================================================
#改變ax.add_feature和ax.coastlines的先後使用順序可實現邊界線的顯示或完全填充覆蓋
ax.coastlines(scale)
#===================================================
#標註座標軸
ax.set_xticks([0, 60, 120, 180, 240, 300, 360], crs=ccrs.PlateCarree())
ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
#zero_direction_label用來設定經度的0度加不加E和W
lon_formatter = LongitudeFormatter(zero_direction_label=False)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)
#新增網格線
gl = ax.gridlines()

fig.savefig('plotmap.png')
# plt.show()