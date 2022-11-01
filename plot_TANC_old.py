import time as t
import datetime as dt
import netCDF4 as nc
import numpy as np
import os
import re
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cartopy.crs as ccrs
from datetime import datetime as dtdt
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

shp_Coastline = 'C:/Users/Showlong/Desktop/Python Tools/shp/natural_earth/physical/10m_coastline.shp'
shp_TWNboundWGS84 = 'C:/Users/Showlong/Desktop/Python Tools/shp/taiwan/gadm36_TWN_0.shp'
shp_TWNcityWGS84 = 'C:/Users/Showlong/Desktop/Python Tools/shp/taiwan/gadm36_TWN_1.shp'
shp_TWNcountyWGS84 = 'C:/Users/Showlong/Desktop/Python Tools/shp/taiwan/gadm36_TWN_2.shp'
shp_CHNboundWGS84 = 'C:/Users/Showlong/Desktop/Python Tools/shp/china/gadm36_CHN_0.shp'
shp_JPNboundWGS84 = 'C:/Users/Showlong/Desktop/Python Tools/shp/japan/gadm36_JPN_0.shp'
shp_PHLboundWGS84 = 'C:/Users/Showlong/Desktop/Python Tools/shp/philippines/gadm36_PHL_0.shp'
shp_TWNcountyTWD97 = 'C:/Users/Showlong/Desktop/Python Tools/shp/taiwan_county/COUNTY_MOI_1090820.shp'
shape_feature_Coastline = ShapelyFeature(Reader(shp_Coastline).geometries(), ccrs.PlateCarree(),
                               linewidth = 1.0 , facecolor = (1. , 1. , 1. , 0.), 
                               edgecolor = 'w' , zorder = 10)
shape_feature_TWNboundWGS84 = ShapelyFeature(Reader(shp_TWNboundWGS84).geometries(), ccrs.PlateCarree(),
                               linewidth = 0.5 , facecolor = (1. , 1. , 1. , 0.), 
                               edgecolor = 'w' , zorder = 10)
shape_feature_TWNcityWGS84 = ShapelyFeature(Reader(shp_TWNcityWGS84).geometries(), ccrs.PlateCarree(),
                               linewidth = 0.2 , facecolor = (1. , 1. , 1. , 0.), 
                               edgecolor = (.3 , .3 , .3 , 1.) , zorder = 10)
shape_feature_TWNcountyWGS84 = ShapelyFeature(Reader(shp_TWNcountyWGS84).geometries(), ccrs.PlateCarree(),
                               linewidth = 0.2 , facecolor = (1. , 1. , 1. , 0.), 
                               edgecolor = (.3 , .3 , .3 , 1.) , zorder = 10)
shape_feature_CHNboundWGS84 = ShapelyFeature(Reader(shp_CHNboundWGS84).geometries(), ccrs.PlateCarree(),
                               linewidth = 0.5 , facecolor = (1. , 1. , 1. , 0.), 
                               edgecolor = 'w' , zorder = 10)
shape_feature_JPNboundWGS84 = ShapelyFeature(Reader(shp_JPNboundWGS84).geometries(), ccrs.PlateCarree(),
                               linewidth = 0.5 , facecolor = (1. , 1. , 1. , 0.), 
                               edgecolor = 'w' , zorder = 10)
shape_feature_PHLboundWGS84 = ShapelyFeature(Reader(shp_PHLboundWGS84).geometries(), ccrs.PlateCarree(),
                               linewidth = 0.5 , facecolor = (1. , 1. , 1. , 0.), 
                               edgecolor = 'w' , zorder = 10)
shape_feature_TWNcountyTWD97 = ShapelyFeature(Reader(shp_TWNcountyTWD97).geometries(), ccrs.PlateCarree(),
                               linewidth = 0.2 , facecolor = (1. , 1. , 1. , 0.), 
                               edgecolor = (.3 , .3 , .3 , 1.) , zorder = 10)

########## Set Date/Time & Field ##########
date_time_start = dtdt(2020 , 8 , 4 , 6 , 0 , 0) # UTC for both TANC & Mosaic
date_time_end = dtdt(2020 , 8 , 4 , 10 , 0 , 0) # UTC for both TANC & Mosaic

field_in = "W"
field_out = field_in
# field_in = "DIV_LI"
# field_out = "LI"

timestamp_start = date_time_start.timestamp()
timestamp_end = date_time_end.timestamp()
timestep = 60 # Unit: Minute

time_lag =  1 # Default (Unit: hours)
lvls_dBZ = [35 , 45 , 55 , 65]

for timestamp in np.arange(timestamp_start , timestamp_end + 1 , timestep * 60):
    Year =      int(dtdt.fromtimestamp(timestamp).strftime("%Y"))
    Month =     int(dtdt.fromtimestamp(timestamp).strftime("%m"))
    Day =       int(dtdt.fromtimestamp(timestamp).strftime("%d"))
    Hour =      int(dtdt.fromtimestamp(timestamp).strftime("%H"))
    Minute =    int(dtdt.fromtimestamp(timestamp).strftime("%M"))
    Second =    int(dtdt.fromtimestamp(timestamp).strftime("%S"))

    date_time = dtdt(Year , Month , Day , Hour , Minute , Second)
    radar_time = date_time + dt.timedelta(hours = time_lag)
    radar_timeLST = radar_time + dt.timedelta(hours = 8)

    dateStringUTC = date_time.strftime("%Y%m%d")
    timeStringUTC = date_time.strftime("%H%M%S")
    rdateStringUTC = radar_time.strftime("%Y%m%d")
    rtimeStringUTC = radar_time.strftime("%H%M%S")
    rdtStringLST = radar_timeLST.strftime("%Y/%m/%d %H:%M:%S")

    filedate = dateStringUTC
    filetime = timeStringUTC
    radardate = rdateStringUTC
    radartime = rtimeStringUTC

    # Set Path
    dir = "C:/Users/Showlong/Desktop/TANC Cases/RWRF_MR/" + field_in + "/" + filedate + "/"
    file = filedate + "_" + filetime + ".nc"
    path = dir + file

    datagrp = nc.Dataset(path)
    print(datagrp)

    # Read Mosaic (Now)
    dBZ = []
    # fi = open("C:/Users/Showlong/Desktop/TANC Cases/Mosaic/" + radardate + "/" + filetime + ".dat", 'r') # No Lag
    fi = open("C:/Users/Showlong/Desktop/TANC Cases/Mosaic/" + radardate + "/" + radartime + ".dat", 'r') # Lag
    lines = fi.readlines()
    fi.close()
    for line in lines:
        dBZ.append(line[19 : 26])
    del dBZ[0]
    dBZ = np.reshape(dBZ , (500 , 400))

    ########## Colormap & Label ##########
    ##### CAPE #####
    # VAR = datagrp.variables['CAPE'][:]
    # color = [
    #     '#191970','#00008b','#0000cd','#4169e1','#00ffff',
    #     '#7fffd4','#00fa9a','#00cd66','#228b22','#adff2f',
    #     '#cdcd00','#eeee00','#ffff00','#ffd700','#ffa500',
    #     '#ff7f50','#ff6347','#ff0000','#ee3b3b','#cd0000'
    # ]
    # title_label = 'CAPE'
    # cbar_label = 'J/kg'
    # lvls = [0.0001, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 10000]
    # lvlsStr = lvls

    ##### CIN #####
    # VAR = datagrp.variables['CIN'][:]
    # color = [
    #     '#00fa9a','#00cd66','#228b22','#ffd700','#ff7f50',
    #     '#ff6347','#ee3b3b','#cd0000'
    # ]
    # title_label = 'CIN'
    # cbar_label = 'J/kg'
    # lvls = [0.0001, 10, 30, 40, 80, 180, 330, 840, 10000]
    # lvlsStr = lvls

    ##### CU #####
    # VAR = datagrp.variables['Final'][:]
    # color = [
    #     '#191970','#00008b','#0000ff','#4169e1','#00ffff',
    #     '#7fffd4','#9acd32','#ffff00','#ffd700','#ffa500',
    #     '#ff0000'
    # ]
    # title_label = 'Cloud Classification'
    # cbar_label = 'interest'
    # lvls = [-1, -0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1]
    # lvlsStr = lvls

    ##### DIV #####
    # VAR = datagrp.variables['Convergence'][:]
    # color = [
    #     '#ff0000','#ff6347','#fa8072','#ffa500','#ffd700',
    #     '#daa520','#b8860b','#a0522d','#8b4513','#696969',
    #     '#006400','#228b22','#32cd32','#3cb371','#6495ed',
    #     '#6a5acd','#0000cd','#0000ff'
    # ]
    # title_label = 'Divergence'
    # cbar_label = '/1e3s'
    # lvls = np.array([-1.2, -1, -0.8, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, -0.02, 0.02, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1, 1.2])
    # lvlsStr = lvls

    ##### FLH #####
    # VAR = datagrp.variables['LIK'][:]
    # color = [
    #     '#404040','#00008b','#0000cd','#6a5acd','#6495ed',
    #     '#48d1cc','#556b2f','#006400','#008b45','#3cb371',
    #     '#32cd32','#7fff00','#caff70','#b8860b','#daa520',
    #     '#ffd700','#ffff00','#a52a2a','#cd0000','#ee3b3b',
    #     '#ff3030','#ff00ff','#bebebe','#d3d3d3','#fffafa'
    # ]
    # title_label = 'Frontal Zone Likelihood'
    # cbar_label = 'interest'
    # lvls = [-100, -0.001, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1, 2, 5, 10, 100]
    # lvlsStr = lvls

    ##### LH #####
    # VAR = datagrp.variables['Init60_rwrf_MR'][:]
    # color = [
    #     '#00008b','#0000cd','#6a5acd','#6495ed','#48d1cc',
    #     '#006400','#556b2f','#008b45','#00cd66','#32cd32',
    #     '#7fff00','#e9967a','#fa8072','#cd6889','#b22222',
    #     '#ff0000','#ff1493'
    # ]
    # title_label = 'Likelihood'
    # cbar_label = 'interest'
    # lvls = [-3, -1, -0.6, -0.3, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 3]
    # lvlsStr = lvls

    ##### LI #####
    # VAR = datagrp.variables['LiftedIndex'][:]
    # color = [
    #     '#191970','#00008b','#0000cd','#4169e1','#00ffff',
    #     '#7fffd4','#00fa9a','#00cd66','#228b22','#adff2f',
    #     '#cdcd00','#eeee00','#ffff00','#ffd700','#ffa500',
    #     '#ff7f50','#ff6347','#ff0000','#ee3b3b','#cd0000'
    # ]
    # title_label = 'Lifted Index'
    # cbar_label = '${^o}$C'
    # lvls = [-30, -27, -24, -21, -18, -15, -12, -9, -6, -3, -1, 1, 3, 6, 9, 12, 15, 18, 21, 24, 27]
    # lvlsStr = lvls

    ##### RH #####
    # VAR = datagrp.variables['rh_avg'][:]
    # color = [
    #     '#cd0000','#ee3b3b','#ff0000','#ff6347','#ff7f50',
    #     '#ffa500','#ffd700','#ffff00','#eeee00','#cdcd00',
    #     '#adff2f','#228b22','#00cd66','#00fa9a','#7fffd4',
    #     '#00ffff','#4169e1','#0000cd','#00008b','#191970'
    # ]
    # title_label = 'RHavg'
    # cbar_label = '%'
    # lvls = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 110]
    # lvlsStr = lvls

    ##### ROC #####
    # VAR = datagrp.variables['Temp_Rate'][:]
    # color = [
    #     '#00008b','#0000cd','#6495ed','#00ffff','#006400',
    #     '#3cb371','#00ff7f','#f5deb3','#b8860b','#ffd700'
    # ]
    # title_label = 'IR Rate of Change'
    # cbar_label = '${^o}$C/15min'
    # lvls = [-40, -24, -20, -16, -12, -8, -4, -2, 2, 8, 20]
    # lvlsStr = lvls

    ##### VSI #####
    # VAR = datagrp.variables['vert_sum'][:]
    # color = [
    #     '#191970','#00008b','#0000ff','#4169e1','#00ffff',
    #     '#7fffd4','#9acd32','#ffff00','#ffd700','#ffa500',
    #     '#ff7f50','#ff4500','#ff0000'
    # ]
    # title_label = 'Vertical Sum Interest'
    # cbar_label = 'interest'
    # lvls = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39]
    # lvlsStr = lvls

    ##### W #####
    VAR = datagrp.variables['w3'][:]
    color = [
        '#ff1493','#b03060','#9932cc','#0000ff','#4169e1',
        '#00bfff','#00fa9a','#228b22','#bebebe','#ee9a49',
        '#ffd700','#ffff00','#ff8c69','#ff6347','#ff4040',
        '#ff0000','#b22222'
    ]
    title_label = 'W'
    cbar_label = 'm/s'
    lvls = np.array([-0.032, -0.028, -0.024, -0.02, -0.016, -0.012, -0.008, -0.004, -0.001, 0.001, 0.004, 0.008, 0.012, 0.016, 0.02, 0.024, 0.028, 0.032]) * 200
    lvlsStr = lvls

    ##### Mosaic #####
    # VAR = dBZ
    # color = [
    #     '#625273','#675775','#6b5c78','#6f617b','#73677e','#776c81','#7b7184','#7f7787','#837c8a','#87818d',
    #     '#8b8690','#8f8c93','#939196','#979699','#9c9c9c','#00cc00','#00c500','#00be00','#00b800','#00b100',
    #     '#00aa00','#00a500','#009f00','#009a00','#009400','#008e00','#33a500','#66bb00','#99d200','#cce800',
    #     '#ffff00','#f9f200','#f4e500','#efd800','#eacc00','#e5bf00','#eab500','#efab00','#f4a200','#f99800',
    #     '#ff8e00','#ff8513','#ff7c26','#ff733a','#ff6a4d','#ff6060','#ff4d4d','#ff3a3a','#ff2626','#ff1313',
    #     '#ff0000','#f50000','#eb0000','#e10000','#d80000','#ce0000','#d80033','#e10066','#eb0099','#f500cc',
    #     '#ff00ff'
    # ]
    # title_label = 'Mosaic'
    # cbar_label = 'dBZ'
    # lvls = np.arange(5 , 67 , 1)
    # lvlsStr = [5 , 10 , 15 , 20 , 25 , 30 , 35 , 40 , 45 , 50 , 55 , 60 , 65]

    # Variables
    time = datagrp.variables['time'][:]
    x0 = datagrp.variables['x0'][:]
    y0 = datagrp.variables['y0'][:]
    z0 = datagrp.variables['z0'][:]
    VAR = VAR.reshape(500 , 400)
    xx , yy = np.meshgrid(x0 , y0)

    struct_time = t.localtime(time)
    dtStringLST = t.strftime("%Y/%m/%d %H:%M:%S", struct_time)
    print(dtStringLST)

    # Plot
    cm = ListedColormap(color)
    norm = BoundaryNorm(lvls , cm.N)

    # matplotlib.use('TkAgg')

    plt.style.use(['dark_background'])
    fig , ax = plt.subplots(figsize = [4.8 , 4.8] , subplot_kw={'projection':ccrs.PlateCarree()})
    # ax.add_feature(shape_feature_TWNcityWGS84)
    # ax.add_feature(shape_feature_TWNcountyWGS84)
    # ax.add_feature(shape_feature_TWNboundWGS84)
    ax.add_feature(shape_feature_TWNcountyTWD97)
    # ax.add_feature(shape_feature_CHNboundWGS84)
    # ax.add_feature(shape_feature_JPNboundWGS84)
    # ax.add_feature(shape_feature_PHLboundWGS84)
    ax.add_feature(shape_feature_Coastline)
    ax.gridlines(draw_labels=False , alpha = 0.5 , 
                xlocs = [118 , 119 , 120 , 121 , 122 , 123 , 124] , 
                ylocs = [20 , 21 , 22 , 23 , 24 , 25 , 26])
    ax.set_extent([119 , 123 , 21 , 26])
    plt.xticks([119 , 120 , 121 , 122 , 123] , ['119${^o}$E' , '120${^o}$E' , '121${^o}$E' , '122${^o}$E' , '123${^o}$E'] , size = 6)
    plt.yticks([21 , 22 , 23 , 24 , 25 , 26] , ['21${^o}$N' , '22${^o}$N' , '23${^o}$N' , '24${^o}$N' , '25${^o}$N' , '26${^o}$N'] , size = 6)
    ax.contour(xx , yy , dBZ , levels = lvls_dBZ , colors = ['#ff00ff'] , linewidths = [0.7 , 0.5 , 0.3 , 0.1])
    CS = ax.contourf(xx , yy , VAR , levels = lvls , cmap = cm , norm = norm , alpha = 1)
    CS.set_clim(min(lvls) , max(lvls))
    # plt.title('TANC - ' + title_label + '\n')
    ax.text(119 , 26.20 , title_label , fontsize = 8 , ha = 'left')
    ax.text(119 , 26.05 , 'Mosaic (35 dBZ)' , fontsize = 8 , ha = 'left' , color = '#ff00ff')
    ax.text(123 , 26.20 , dtStringLST + ' LST' , fontsize = 8 , ha = 'right')
    ax.text(123 , 26.05 , rdtStringLST + ' LST' , fontsize = 8 , ha = 'right' , color = '#ff00ff')
    cbar = plt.colorbar(CS , orientation = 'vertical', ticks = lvlsStr)
    # cbar = plt.colorbar(CS , orientation = 'vertical', ticks = lvlsStr , format = '%.3f')
    cbar.ax.tick_params(labelsize = 6)
    cbar.set_label(cbar_label , size = 6)
    # plt.show()
    fig.savefig("C:/Users/Showlong/Desktop/Python Tools/output/RWRF_MR/" + filedate + "/" + field_out + "_" + filedate + "_" + filetime + ".png" , dpi = 200)




# def WGS84FromTWD67TM2(x,y):
#    out = {'status':False}
#    lat = None
#    lon = None
   
#    # TWD67 to TWD97
#    A = 0.00001549
#    B = 0.000006521
#    x = float(x)
#    y = float(y)
#    x = x + 807.8 + A * x + B * y
#    y = y - 248.6 + A * y + B * x

#    # TWD97 to WGS84
#    result = os.popen('echo '+str(x)+' '+str(y)+' | proj -I +proj=tmerc +ellps=GRS80 +lon_0=121 +x_0=250000 +k=0.9999 -f "%.8f"').read().strip() # lat, lng 格式, 不必再轉換
#    process = re.compile( '([0-9]+\.[0-9]+)', re.DOTALL )
#    for item in process.findall(result):
#       if lon == None:
#          lon = float(item)
#       elif lat == None:
#          lat = float(item)
#       else:
#          break

#    # result = os.popen('echo '+str(x)+' '+str(y)+' | proj -I +proj=tmerc +ellps=GRS80 +lon_0=121 +x_0=250000 +k=0.9999').read().strip() # 分度秒格式

#    # 分度秒格式轉換
#    #process = re.compile( "([0-9]+)d([0-9]+)'([0-9\.]+)\"E\t([0-9]+)d([0-9]+)'([0-9\.]+)", re.DOTALL )
#    #for item in process.findall(result):
#    #    lon = float(item[0]) + ( float(item[1]) + float(item[2])/60 )/60
#    #    lat = float(item[3]) + ( float(item[4]) + float(item[5])/60 )/60
#    #    break
#    if lat == None or lon == None:
#       return out
#    out['lat'] = lat
#    out['lng'] = lon
#    out['status'] = True
#    return out

# print(WGS84FromTWD67TM2(119 , 21))