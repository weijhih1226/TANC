########## plot_RWRF_WS.py ##########
####### Author: Wei-Jhih Chen #######
######## Update: 2021/04/01 #########

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
import configparser as cp
from datetime import datetime as dtdt
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from scipy import io

########## Set Directory & Date/Time & Fields ##########
model = 'rwrf'
mode = "WS"
cfgPath = './cfg/path.cfg'
cfg = cp.RawConfigParser()
cfg.read(cfgPath)
home_inDir = cfg.get(model + '-' + mode , 'home_inDir')
home_inDirR = cfg.get(model + '-' + mode , 'home_inDirR')
home_outDir = cfg.get(model + '-' + mode , 'home_outDir')
home_outDirR = cfg.get(model + '-' + mode , 'home_outDirR')

date_time_start = dtdt(2021 , 3 , 6 , 0 , 0 , 0) # UTC for both TANC & Mosaic
date_time_end = dtdt(2021 , 3 , 6 , 23 , 0 , 0) # UTC for both TANC & Mosaic

field_in = ["cape" , "cin" , "climate" , "trend" , "div" , "Init60" , "dbz" , "rh" , "loc"]
field_out = ["CAPE" , "CIN" , "CF" , "CT" , "DIV" , "LH" , "RC" , "RH" , "SIL"]
# field_in = ["climate" , "trend" , "div" , "Init60" , "dbz" , "loc"]
# field_out = ["CF" , "CT" , "DIV" , "LH" , "RC" , "SIL"]
# field_in = ["trend"]
# field_out = ["CT"]

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

########## For Input Mode ##########
# inSYear = int(input("??????????????????(e.g. 2021)???"))
# inSMonth = int(input("??????????????????(e.g. 1)???"))
# inSDay = int(input("??????????????????(e.g. 1)???"))
# inSHour = int(input("??????????????????(UTC)(e.g. 0)???"))
# inSMinute = int(input("??????????????????(e.g. 0)???"))
# inSSecond = int(input("??????????????????(e.g. 0)???"))

# inEYear = int(input("??????????????????(e.g. 2021)???"))
# inEMonth = int(input("??????????????????(e.g. 1)???"))
# inEDay = int(input("??????????????????(e.g. 2)???"))
# inEHour = int(input("??????????????????(UTC)(e.g. 23)???"))
# inEMinute = int(input("??????????????????(e.g. 0)???"))
# inESecond = int(input("??????????????????(e.g. 0)???"))

# date_time_start = dtdt(inSYear , inSMonth , inSDay , inSHour , inSMinute , inSSecond) # UTC for both TANC & Mosaic
# date_time_end = dtdt(inEYear , inEMonth , inEDay , inEHour , inEMinute , inESecond) # UTC for both TANC & Mosaic

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
    date_timeLST = date_time + dt.timedelta(hours = 8)
    radar_timeLST = radar_time + dt.timedelta(hours = 8)

    dateStringUTC = date_time.strftime("%Y%m%d")
    timeStringUTC = date_time.strftime("%H%M%S")
    rdateStringUTC = radar_time.strftime("%Y%m%d")
    rtimeStringUTC = radar_time.strftime("%H%M%S")
    dtStringLST = date_timeLST.strftime("%Y/%m/%d %H:%M:%S")
    rdtStringLST = radar_timeLST.strftime("%Y/%m/%d %H:%M:%S")

    filedate = dateStringUTC
    filetime = timeStringUTC
    radardate = rdateStringUTC
    radartime = rtimeStringUTC

    # Set Path
    inRDir = home_inDirR + radardate + '/'
    inRPath = inRDir + radardate + '_' + radartime + '.nc'
    outDir = home_outDir + filedate + '/'
    outRDir = home_outDirR + radardate + '/'
    outRPath = outRDir + radardate + '_' + radartime + '.png'

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

    # Read Mosaic .dat (Lag)
    # dBZ = []
    # fi = open("./cases/Mosaic/dat/" + radardate + "/" + radartime + ".dat", 'r')
    # lines = fi.readlines()
    # fi.close()
    # for line in lines:
    #     dBZ.append(line[19 : 26])
    # del dBZ[0]
    # dBZ = np.reshape(dBZ , (500 , 400))

    # Read Mosaic .nc (Lag)
    if not(os.path.isfile(inRPath)):
        continue
    datagrpR = nc.Dataset(inRPath)
    x0R = datagrpR.variables['x0'][:]
    y0R = datagrpR.variables['y0'][:]
    dBZ = datagrpR.variables['DBZ'][:]
    dBZ = dBZ.reshape(500 , 400)
    xxR , yyR = np.meshgrid(x0R , y0R)
    dBZ[dBZ == -99.0] = float('nan')

    # Read Field
    for cnt_field in np.arange(0 , len(field_in)):
        # Set Path
        if field_out[cnt_field] == 'CF':
            if Hour > 3 and Hour < 13:
                inDir = home_inDir + field_in[cnt_field] + '/'
                inFile = filetime + '.nc'
            else:
                continue
        elif field_out[cnt_field] == 'CT':
            if Hour > 3 and Hour < 12:
                inDir = home_inDir + field_in[cnt_field] + '/'
                inFile = filetime + '.nc'
            else:
                continue
        else:
            inDir = home_inDir + field_in[cnt_field] + '/' + filedate + '/'
            inFile = filedate + '_' + filetime + '.nc'
        inPath = inDir + inFile
        if not(os.path.isfile(inPath)):
            continue
        outPath = outDir + field_out[cnt_field] + "_" + filedate + "_" + filetime + ".png"
        datagrp = nc.Dataset(inPath)

        ########## Colormap & Label ##########
        if field_out[cnt_field] == "CAPE":
            ##### CAPE #####
            VAR = datagrp.variables['CAPE_3D'][:]
            color = [
            '#191970','#00008b','#0000cd','#4169e1','#00ffff',
            '#7fffd4','#00fa9a','#00cd66','#228b22','#adff2f',
            '#cdcd00','#eeee00','#ffff00','#ffd700','#ffa500',
            '#ff7f50','#ff6347','#ff0000','#ee3b3b','#cd0000'
            ]
            title_label = 'CAPE'
            cbar_label = 'J/kg'
            lvls = [0.0001, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 10000]
            lvlsStr = lvls
        elif field_out[cnt_field] == "CIN":
            ##### CIN #####
            VAR = datagrp.variables['CIN_3D'][:]
            color = [
                '#00fa9a','#00cd66','#228b22','#ffd700','#ff7f50',
                '#ff6347','#ee3b3b','#cd0000'
            ]
            title_label = 'CIN'
            cbar_label = 'J/kg'
            lvls = [0.0001, 10, 30, 40, 80, 180, 330, 840, 10000]
            lvlsStr = lvls
        elif field_out[cnt_field] == "CF":
            ##### CF #####
            VAR = datagrp.variables['freq'][:]
            color = [
                '#006400','#556b2f','#228b22','#00cd66','#3cb371',
                '#66cdaa','#7b68ee','#0000ff','#00008b','#68228b',
                '#8b3a62','#b03060','#8b2252','#a0522d','#d2691e',
                '#daa520','#ffff00','#e9967a','#fa8072','#ee2c2c',
                '#ff1493','#d3d3d3','#fffafa','#7f7f7f'
            ]
            title_label = 'Radar ClimoFrequency'
            cbar_label = ''
            lvls = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 80]
            lvlsStr = lvls
        elif field_out[cnt_field] == "CT":
            ##### CT #####
            VAR = datagrp.variables['change'][:]
            color = [
                '#68228b','#00008b','#7b68ee','#add8e6','#006400',
                '#556b2f','#66cdaa','#cccccc','#eedd82','#daa520',
                '#d2691e','#a0522d','#fa8072','#ff1493','#8b2252'
            ]
            title_label = 'Radar ClimoTrend'
            cbar_label = ''
            lvls = [-20, -7.5, -5, -4, -3, -2, -1, -0.5, 0.5, 1, 2, 3, 4, 5, 7.5, 20]
            lvlsStr = lvls
        elif field_out[cnt_field] == "DIV":
            ##### DIV #####
            VAR = datagrp.variables['Convergence'][:]
            color = [
                '#ff0000','#ff6347','#fa8072','#ffa500','#ffd700',
                '#daa520','#b8860b','#a0522d','#8b4513','#696969',
                '#006400','#228b22','#32cd32','#3cb371','#6495ed',
                '#6a5acd','#0000cd','#0000ff'
            ]
            title_label = 'Divergence'
            cbar_label = '/1e3s'
            lvls = np.array([-1.2, -1, -0.8, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, -0.02, 0.02, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1, 1.2])
            lvlsStr = lvls
        elif field_out[cnt_field] == "LH":
            ##### LH #####
            VAR = datagrp.variables['Init60_rwrf_WS'][:]
            color = [
                '#00008b','#0000cd','#6a5acd','#6495ed','#48d1cc',
                '#006400','#556b2f','#008b45','#00cd66','#32cd32',
                '#7fff00','#e9967a','#fa8072','#cd6889','#b22222',
                '#ff0000','#ff1493'
            ]
            title_label = 'Likelihood'
            cbar_label = 'interest'
            lvls = [-3, -1, -0.6, -0.3, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 3]
            lvlsStr = lvls
        elif field_out[cnt_field] == "RH":
            ##### RH #####
            VAR = datagrp.variables['RH_avg'][:]
            color = [
                '#cd0000','#ee3b3b','#ff0000','#ff6347','#ff7f50',
                '#ffa500','#ffd700','#ffff00','#eeee00','#cdcd00',
                '#adff2f','#228b22','#00cd66','#00fa9a','#7fffd4',
                '#00ffff','#4169e1','#0000cd','#00008b','#191970'
            ]
            title_label = 'RHavg'
            cbar_label = '%'
            lvls = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 110]
            lvlsStr = lvls
        elif field_out[cnt_field] == "RC":
            ##### RC #####
            VAR = datagrp.variables['conv_partitione'][:]
            color = [
                '#006400','#556b2f','#228b22','#00cd66','#3cb371',
                '#66cdaa','#7b68ee','#0000ff','#00008b','#68228b',
                '#8b3a62','#b03060','#8b2252','#a0522d','#d2691e',
                '#daa520','#ffff00','#e9967a','#fa8072','#ee2c2c',
                '#ff1493','#d3d3d3','#fffafa'
            ]
            title_label = 'RadarCuAdvect'
            cbar_label = 'dBZ'
            lvls = [-40, -10, -6, -3, 0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 31, 35, 40, 45, 50, 55, 60, 65, 70, 80]
            lvlsStr = lvls
        elif field_out[cnt_field] == "SIL":
            ##### SIL #####
            VAR = datagrp.variables['initWeight'][:]
            color = [
                '#000000','#0d0d0d','#1c1c1c','#363636','#404040',
                '#4d4d4d','#575757','#696969','#787878','#828282',
                '#878787','#999999','#a6a6a6','#b3b3b3','#bfbfbf',
                '#cccccc','#d9d9d9','#e5e5e5','#f2f2f2','#fffafa',
                '#ff1493','#b03060','#9932cc','#0000ff','#4169e1',
                '#00bfff','#00fa9a','#228b22','#bebebe','#ee9a49',
                '#ffd700','#ffff00','#ff8c69','#ff6347','#ff4040',
                '#ff0000','#b22222'
            ]
            title_label = 'StormInitLoc'
            cbar_label = ''
            lvls = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7]
            lvlsStr = lvls
        else:
            break
        
        # Variables
        time = np.double(datagrp.variables['time'][:])
        x0 = datagrp.variables['x0'][:]
        y0 = datagrp.variables['y0'][:]
        VAR = VAR.reshape(500 , 400)
        xx , yy = np.meshgrid(x0 , y0)

        struct_time = t.localtime(time)
        timeStringLST = t.strftime("%Y/%m/%d %H:%M:%S", struct_time)

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
        ax.contour(xxR , yyR , dBZ , levels = lvls_dBZ , colors = ['#ff00ff'] , linewidths = [0.7 , 0.5 , 0.3 , 0.1])
        CS = ax.contourf(xx , yy , VAR , levels = lvls , cmap = cm , norm = norm , alpha = 1)
        CS.set_clim(min(lvls) , max(lvls))
        ax.text(119 , 26.35 , model.upper() + "_" + mode , fontsize = 6 , ha = 'left' , color = '#888888')
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
    x0 = io.loadmat('./mat/lonlat.mat')['x0']
    y0 = io.loadmat('./mat/lonlat.mat')['y0']
    xx , yy = np.meshgrid(x0 , y0)

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
    CS = ax.contourf(xxR , yyR , dBZ , levels = lvls , cmap = cm , norm = norm , alpha = 1)
    CS.set_clim(min(lvls) , max(lvls))
    ax.text(119 , 26.05 , title_label , fontsize = 8 , ha = 'left')
    ax.text(123 , 26.05 , rdtStringLST + ' LST' , fontsize = 8 , ha = 'right')
    cbar = plt.colorbar(CS , orientation = 'vertical', ticks = lvlsStr)
    cbar.ax.tick_params(labelsize = 6)
    cbar.set_label(cbar_label , size = 6)
    fig.savefig(outRPath , dpi = 200)
    print(rdtStringLST + "L" , "- Mosaic has been saved!")

# io.savemat('./mat/lonlat.mat' , {'x0': x0 , 'y0': y0})