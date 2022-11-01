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
import configparser
from datetime import datetime as dtdt
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

########## Configuration ##########
configPath = './cfg/parm.cfg'
conf = configparser.RawConfigParser()
conf.read(configPath)

########## Shapefiles ##########
shp_Coastline = './shp/natural_earth/physical/10m_coastline.shp'
shp_TWNboundWGS84 = './shp/taiwan/gadm36_TWN_0.shp'
shp_TWNcityWGS84 = './shp/taiwan/gadm36_TWN_1.shp'
shp_TWNcountyWGS84 = './shp/taiwan/gadm36_TWN_2.shp'
shp_CHNboundWGS84 = './shp/china/gadm36_CHN_0.shp'
shp_JPNboundWGS84 = './shp/japan/gadm36_JPN_0.shp'
shp_PHLboundWGS84 = './shp/philippines/gadm36_PHL_0.shp'
shp_TWNcountyTWD97 = './shp/taiwan_county/COUNTY_MOI_1090820.shp'
shape_feature_Coastline = ShapelyFeature(Reader(shp_Coastline).geometries(), ccrs.PlateCarree(),
                               linewidth = 1.0 , facecolor = (1. , 1. , 1. , 0.), 
                               edgecolor = 'w' , zorder = 10)
shape_feature_TWNcountyTWD97 = ShapelyFeature(Reader(shp_TWNcountyTWD97).geometries(), ccrs.PlateCarree(),
                               linewidth = 0.2 , facecolor = (1. , 1. , 1. , 0.), 
                               edgecolor = (.3 , .3 , .3 , 1.) , zorder = 10)
# shape_feature_TWNboundWGS84 = ShapelyFeature(Reader(shp_TWNboundWGS84).geometries(), ccrs.PlateCarree(),
#                                linewidth = 0.5 , facecolor = (1. , 1. , 1. , 0.), 
#                                edgecolor = 'w' , zorder = 10)
# shape_feature_TWNcityWGS84 = ShapelyFeature(Reader(shp_TWNcityWGS84).geometries(), ccrs.PlateCarree(),
#                                linewidth = 0.2 , facecolor = (1. , 1. , 1. , 0.), 
#                                edgecolor = (.3 , .3 , .3 , 1.) , zorder = 10)
# shape_feature_TWNcountyWGS84 = ShapelyFeature(Reader(shp_TWNcountyWGS84).geometries(), ccrs.PlateCarree(),
#                                linewidth = 0.2 , facecolor = (1. , 1. , 1. , 0.), 
#                                edgecolor = (.3 , .3 , .3 , 1.) , zorder = 10)
# shape_feature_CHNboundWGS84 = ShapelyFeature(Reader(shp_CHNboundWGS84).geometries(), ccrs.PlateCarree(),
#                                linewidth = 0.5 , facecolor = (1. , 1. , 1. , 0.), 
#                                edgecolor = 'w' , zorder = 10)
# shape_feature_JPNboundWGS84 = ShapelyFeature(Reader(shp_JPNboundWGS84).geometries(), ccrs.PlateCarree(),
#                                linewidth = 0.5 , facecolor = (1. , 1. , 1. , 0.), 
#                                edgecolor = 'w' , zorder = 10)
# shape_feature_PHLboundWGS84 = ShapelyFeature(Reader(shp_PHLboundWGS84).geometries(), ccrs.PlateCarree(),
                            #    linewidth = 0.5 , facecolor = (1. , 1. , 1. , 0.), 
                            #    edgecolor = 'w' , zorder = 10)

########## Set Date/Time & Field ##########
# inSYear = int(input("請輸入開始年(e.g. 2021)："))
# inSMonth = int(input("請輸入開始月(e.g. 1)："))
# inSDay = int(input("請輸入開始日(e.g. 1)："))
# inSHour = int(input("請輸入開始時(UTC)(e.g. 0)："))
# inSMinute = int(input("請輸入開始分(e.g. 0)："))
# inSSecond = int(input("請輸入開始秒(e.g. 0)："))

# inEYear = int(input("請輸入結束年(e.g. 2021)："))
# inEMonth = int(input("請輸入結束月(e.g. 1)："))
# inEDay = int(input("請輸入結束日(e.g. 2)："))
# inEHour = int(input("請輸入結束時(UTC)(e.g. 23)："))
# inEMinute = int(input("請輸入結束分(e.g. 0)："))
# inESecond = int(input("請輸入結束秒(e.g. 0)："))

# date_time_start = dtdt(inSYear , inSMonth , inSDay , inSHour , inSMinute , inSSecond) # UTC for both TANC & Mosaic
# date_time_end = dtdt(inEYear , inEMonth , inEDay , inEHour , inEMinute , inESecond) # UTC for both TANC & Mosaic

date_time_start = dtdt(2021 , 3 , 1 , 0 , 0 , 0) # UTC for both TANC & Mosaic
date_time_end = dtdt(2021 , 3 , 1 , 0 , 0 , 0) # UTC for both TANC & Mosaic

field_in = ["CAPE" , "CIN" , "CU" , "DIV_LI" , "FLH" , "LH" , "DIV_LI" , "RH" , "ROC" , "VSI" , "W"]
field_out = ["CAPE" , "CIN" , "CU" , "DIV" , "FLH" , "LH" , "LI" , "RH" , "ROC" , "VSI" , "W"]
# field_in = ["CU" , "DIV_LI" , "LH" , "DIV_LI" , "ROC"]
# field_out = ["CU" , "DIV" , "LH" , "LI" , "ROC"]
# field_in = ["W"]
# field_out = ["W"]

model = "RWRF"
mode = "MR"

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
    outDir = "./output/" + model + "_" + mode + "/" + filedate + "/"
    outRDir = "./output/Mosaic/" + radardate + "/"
    outRPath = outRDir + radardate + "_" + radartime + ".png"

    # Create Directory
    if not(os.path.isdir(outDir)):
        os.mkdir(outDir)
        print ("Successfully created the directory %s " % outDir)
    if not(os.path.isdir(outRDir)):
        os.mkdir(outRDir)
        print ("Successfully created the directory %s " % outRDir)

    # try:
    #     os.mkdir(outDir)
    # except OSError as error:
    #     print (error)
    # else:
    #     print ("Successfully created the directory %s " % outDir)
    # try:
    #     os.mkdir(outRDir)
    # except OSError as error:
    #     print (error)
    # else:
    #     print ("Successfully created the directory %s " % outRDir)

    # Read Mosaic (Lag)
    dBZ = []
    fi = open("./cases/Mosaic/" + radardate + "/" + radartime + ".dat", 'r')
    lines = fi.readlines()
    fi.close()
    for line in lines:
        dBZ.append(line[19 : 26])
    del dBZ[0]
    dBZ = np.reshape(dBZ , (500 , 400))

    # Read Field
    for cnt_field in np.arange(0 , len(field_in)):
        # Set Path
        inDir = "./cases/" + model + "_" + mode + "/" + field_in[cnt_field] + "/" + filedate + "/"
        inFile = filedate + "_" + filetime + ".nc"
        inPath = inDir + inFile
        outPath = outDir + field_out[cnt_field] + "_" + filedate + "_" + filetime + ".png"

        if not(os.path.isfile(inPath)):
            continue
        
        datagrp = nc.Dataset(inPath)

        ########## Colormap & Label ##########
        VAR = datagrp.variables[conf.get(field_out[cnt_field] , "VAR")][:]
        title_label = conf.get(field_out[cnt_field] , "title_label")
        cbar_label = conf.get(field_out[cnt_field] , "cbar_label")
        exec("color = " + conf.get(field_out[cnt_field] , "color"))
        exec("lvls = " + conf.get(field_out[cnt_field] , "lvls"))
        lvlsStr = lvls
        
        # Variables
        time = datagrp.variables['time'][:]
        x0 = datagrp.variables['x0'][:]
        y0 = datagrp.variables['y0'][:]
        z0 = datagrp.variables['z0'][:]
        VAR = VAR.reshape(500 , 400)
        xx , yy = np.meshgrid(x0 , y0)

        struct_time = t.localtime(time)
        dtStringLST = t.strftime("%Y/%m/%d %H:%M:%S", struct_time)

        # Plot
        cm = ListedColormap(color)
        norm = BoundaryNorm(lvls , cm.N)
        # matplotlib.use('TkAgg')

        plt.close()
        plt.style.use(['dark_background'])
        fig , ax = plt.subplots(figsize = [4.8 , 4.8] , subplot_kw={'projection':ccrs.PlateCarree()})
        ax.add_feature(shape_feature_TWNcountyTWD97)
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
        ax.text(119 , 26.35 , model + "_" + mode , fontsize = 6 , ha = 'left' , color = '#888888')
        ax.text(119 , 26.20 , title_label , fontsize = 8 , ha = 'left')
        ax.text(119 , 26.05 , 'Mosaic (35 dBZ)' , fontsize = 8 , ha = 'left' , color = '#ff00ff')
        ax.text(123 , 26.20 , dtStringLST + ' LST' , fontsize = 8 , ha = 'right')
        ax.text(123 , 26.05 , rdtStringLST + ' LST' , fontsize = 8 , ha = 'right' , color = '#ff00ff')
        if field_out[cnt_field] == "FLH":
            cbar = plt.colorbar(CS , orientation = 'vertical', ticks = lvlsStr , format = '%.3f')
        else:
            cbar = plt.colorbar(CS , orientation = 'vertical', ticks = lvlsStr)
        cbar.ax.tick_params(labelsize = 6)
        cbar.set_label(cbar_label , size = 6)
        fig.savefig(outPath , dpi = 200)
        print(dtStringLST + "L" , "-" , field_out[cnt_field] , "has been saved!")

    ##### Mosaic #####
    color = [
        '#625273','#675775','#6b5c78','#6f617b','#73677e','#776c81','#7b7184','#7f7787','#837c8a','#87818d',
        '#8b8690','#8f8c93','#939196','#979699','#9c9c9c','#00cc00','#00c500','#00be00','#00b800','#00b100',
        '#00aa00','#00a500','#009f00','#009a00','#009400','#008e00','#33a500','#66bb00','#99d200','#cce800',
        '#ffff00','#f9f200','#f4e500','#efd800','#eacc00','#e5bf00','#eab500','#efab00','#f4a200','#f99800',
        '#ff8e00','#ff8513','#ff7c26','#ff733a','#ff6a4d','#ff6060','#ff4d4d','#ff3a3a','#ff2626','#ff1313',
        '#ff0000','#f50000','#eb0000','#e10000','#d80000','#ce0000','#d80033','#e10066','#eb0099','#f500cc',
        '#ff00ff'
    ]
    title_label = 'Mosaic'
    cbar_label = 'dBZ'
    lvls = np.arange(5 , 67 , 1)
    lvlsStr = [5 , 10 , 15 , 20 , 25 , 30 , 35 , 40 , 45 , 50 , 55 , 60 , 65]

    cm = ListedColormap(color)
    norm = BoundaryNorm(lvls , cm.N)

    plt.close()
    plt.style.use(['dark_background'])
    fig , ax = plt.subplots(figsize = [4.8 , 4.8] , subplot_kw = {'projection':ccrs.PlateCarree()})
    ax.add_feature(shape_feature_TWNcountyTWD97)
    ax.add_feature(shape_feature_Coastline)
    ax.gridlines(draw_labels=False , alpha = 0.5 , 
                xlocs = [118 , 119 , 120 , 121 , 122 , 123 , 124] , 
                ylocs = [20 , 21 , 22 , 23 , 24 , 25 , 26])
    ax.set_extent([119 , 123 , 21 , 26])
    plt.xticks([119 , 120 , 121 , 122 , 123] , ['119${^o}$E' , '120${^o}$E' , '121${^o}$E' , '122${^o}$E' , '123${^o}$E'] , size = 6)
    plt.yticks([21 , 22 , 23 , 24 , 25 , 26] , ['21${^o}$N' , '22${^o}$N' , '23${^o}$N' , '24${^o}$N' , '25${^o}$N' , '26${^o}$N'] , size = 6)
    CS = ax.contourf(xx , yy , dBZ , levels = lvls , cmap = cm , norm = norm , alpha = 1)
    CS.set_clim(min(lvls) , max(lvls))
    ax.text(119 , 26.05 , title_label , fontsize = 8 , ha = 'left')
    ax.text(123 , 26.05 , rdtStringLST + ' LST' , fontsize = 8 , ha = 'right')
    cbar = plt.colorbar(CS , orientation = 'vertical', ticks = lvlsStr)
    cbar.ax.tick_params(labelsize = 6)
    cbar.set_label(cbar_label , size = 6)
    fig.savefig(outRPath , dpi = 200)
    print(rdtStringLST + "L" , "- Mosaic has been saved!")



class switch(object):
    def __init__(self , case_path):
        self.switch_to = case_path
        self._invoked = False

    def case(self , key , method):
        if self.switch_to == key and not self._invoked:
            self._invoked = True
            method()

        return self

    def default(self , method):
        if not self._invoked:
            self._invoked = True
            method()