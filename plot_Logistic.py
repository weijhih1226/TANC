########################################
########### plot_Logistic.py ###########
######## Author: Wei-Jhih Chen #########
########## Update: 2021/08/27 ##########
########################################

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
from scipy.interpolate import griddata

########## Set Model & Case & Date/Time ##########
# model = ['RWRF_ANC_WS' , 'RWRF_NO_ANC_WS' , 'RWRF_NO_ANC_WS_WISS']
# model = ['RWRF_ANC_WS']
# model = ['RWRF_NO_ANC_WS']
model = ['RWRF_NO_ANC_WS_WISS']

########## Set Case ##########
case_year = '2021'
# case_date = ['0510' , '0513' , '0518' , '0519' , '0523' , '0609' , '0610' , '0611' , '0612' , '0703' , '0708' , '0709' , '0711' , '0718' , '0729' , '0811' , '0814' , '0815' , '0816' , '0820' , '0821' , '0824']
case_date = ['1002']

for cnt_c in range(0 , len(case_date)):
    ########## Set Date/Time ##########
    date_time_start = dtdt(int(case_year) , int(case_date[cnt_c][0 : 2]) , int(case_date[cnt_c][2 : 4]) , 0 , 0 , 0) # UTC
    date_time_end = dtdt(int(case_year) , int(case_date[cnt_c][0 : 2]) , int(case_date[cnt_c][2 : 4]) , 23 , 50 , 0) # UTC

    timestamp_start = date_time_start.timestamp()
    timestamp_end = date_time_end.timestamp()
    timestep = 10 # Unit: Minute
    time_lag = 1 # Default (Unit: hours)

    ########## Set Path ##########
    map_path = './ref/5_group_Kmeans_labels_smooth.dat'

    ########## Shapefiles ##########
    # shp_Coastline = './shp/natural_earth/physical/10m_coastline.shp'
    shp_TWNcountyTWD97 = './shp/taiwan_county/COUNTY_MOI_1090820.shp'
    # shape_feature_Coastline = ShapelyFeature(Reader(shp_Coastline).geometries(), ccrs.PlateCarree(),
    #                                linewidth = 1.0 , facecolor = (1. , 1. , 1. , 0.), 
    #                                edgecolor = (.3 , .3 , .3 , 1.) , zorder = 10)
    shape_feature_TWNcountyTWD97 = ShapelyFeature(Reader(shp_TWNcountyTWD97).geometries(), ccrs.PlateCarree(),
                                linewidth = 0.5 , facecolor = (1. , 1. , 1. , 0.), 
                                edgecolor = 'k' , zorder = 10)

    ########## Color ##########
    color = ['#fefefe','#c2ddeb','#2a72b1','#f9eae1','#f9cbb2','#ef9b7b','#d6624f','#b82632','#810923']
    lvls = np.array([0 , 0.075 , 0.125 , 0.250 , 0.375 , 0.500 , 0.625 , 0.750 , 0.875 , 1.000]) * 100
    lvls_dBZ = 35
    cm = ListedColormap(color)
    norm = BoundaryNorm(lvls , cm.N)

    ########## Map ##########
    lon_land = []
    lat_land = []
    x_land = []
    y_land = []
    file = open(map_path)
    for line in file:
        lon_land.append(float(line.strip().split('  ')[1].split(' ')[1]))
        lat_land.append(float(line.strip().split('  ')[1].split(' ')[0]))
        x_land.append(int(line.strip().split('  ')[4]))
        y_land.append(int(line.strip().split('  ')[5]))
    file.close()

    ########## Model Loop ##########
    for cnt_m in np.arange(0 , len(model)):
        ########## Set Path ##########
        home_inDir = '/mnt/logistic/' + model[cnt_m] + '/OUTPUT/'
        home_inDirR = '/mnt/mdlanc/nc/stratiform_filter/'
        home_outDir = './output/logistic/' + model[cnt_m] + '/'

        # home_inDir = './cases/logistic/' + model[cnt_m] + '/'
        # home_inDirR = './cases/stratiform_filter/'
        # home_outDir = './output/logistic/' + model[cnt_m] + '/'

        ########## Time Loop ##########
        for timestamp in np.arange(timestamp_start , timestamp_end + 1 , timestep * 60):
            ##### Set Date/Time #####
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
            dtStringLST = date_timeLST.strftime("%Y/%m/%d %H:%M")
            rdtStringLST = radar_timeLST.strftime("%H:%M")

            filedate = dateStringUTC
            filetime = timeStringUTC
            radardate = rdateStringUTC
            radartime = rtimeStringUTC

            ##### Set Path #####
            inPath = home_inDir + filedate + '/' + filetime + '.dat'
            inRPath = home_inDirR + radardate + '/' + radardate + '_' + radartime + '.nc'
            outDir = home_outDir + filedate + '/'
            outPath = outDir + filedate + "_" + filetime + ".png"

            # Create Directory & Skip No File
            if not(os.path.isdir(outDir)):
                os.makedirs(outDir)
                print ("Successfully created the directory %s " % outDir)
            if not(os.path.isfile(inPath)):
                print('No File:' , inPath)
                continue
            if not(os.path.isfile(inRPath)):
                print('No File:' , inRPath)
                continue

            ##### Read Data #####
            Prob = []
            file = open(inPath)
            for line in file:
                Prob.append(float(line.strip()))
            file.close()

            lon_land = np.array(lon_land)
            lat_land = np.array(lat_land)
            Prob = np.array(Prob)

            Prob[Prob == -9999.0] = float('nan')
            Prob = Prob * 100

            ##### Read Radar #####
            try:
                datagrpR = nc.Dataset(inRPath)
            except OSError:
                continue
            x0R = datagrpR.variables['x0'][:]
            y0R = datagrpR.variables['y0'][:]
            dBZ = datagrpR.variables['DBZ'][:]
            dBZ = dBZ.reshape(500 , 400)
            xxR , yyR = np.meshgrid(x0R , y0R)

            # Sea Mask
            dBZ_land = np.empty((len(y0R) , len(x0R)))
            dBZ_land[:] = np.nan
            for cnt_g in range(0 , len(x_land)):
                dBZ_land[y_land[cnt_g] , x_land[cnt_g]] = dBZ[y_land[cnt_g] , x_land[cnt_g]]

            # 35 dBZ Mask
            xxRS = []
            yyRS = []
            for cnt_y in range(0 , len(y0R) , 3):
                for cnt_x in range(0 , len(x0R) , 3):
                    if dBZ_land[cnt_y , cnt_x] >= 35:
                        xxRS.append(xxR[cnt_y , cnt_x])
                        yyRS.append(yyR[cnt_y , cnt_x])

            ##### Set Grid #####
            # option = {}
            # option['lats'] , option['late'] , option['lons'] , option['lone'] = 21.8 , 25.4 , 120 , 122
            # yi = np.arange(float(option['lats']) , float(option['late']) + 0.001 , 0.001)
            # xi = np.arange(float(option['lons']) , float(option['lone']) + 0.001 , 0.001)
            # xx , yy = np.meshgrid(xi , yi)
            # ProbG = griddata((lon_land , lat_land) , Prob , (xx , yy) , method = 'linear')
            ProbG = griddata((lon_land , lat_land) , Prob , (xxR , yyR) , method = 'linear')

            # Sea Mask
            ProbG_land = np.empty((len(y0R) , len(x0R)))
            ProbG_land[:] = np.nan
            for cnt_g in range(0 , len(x_land)):
                ProbG_land[y_land[cnt_g] , x_land[cnt_g]] = ProbG[y_land[cnt_g] , x_land[cnt_g]]

            ########## Plot ##########
            plt.close()
            fig , ax = plt.subplots(figsize = [4.8 , 4.8] , subplot_kw = {'projection':ccrs.PlateCarree()})
            ax.add_feature(shape_feature_TWNcountyTWD97)
            # ax.add_feature(shape_feature_Coastline)
            # ax.gridlines(draw_labels=False , alpha = 0.5 , 
            #             xlocs = [120 , 121 , 122] , 
            #             ylocs = [21 , 22 , 23 , 24 , 25 , 26])
            ax.set_extent([119.8 , 122.2 , 21.8 , 25.4])
            plt.xticks([120 , 121 , 122] , ['120${^o}$E' , '121${^o}$E' , '122${^o}$E'] , size = 6)
            plt.yticks([22 , 23 , 24 , 25] , ['22${^o}$N' , '23${^o}$N' , '24${^o}$N' , '25${^o}$N'] , size = 6)
            # CTF = ax.contourf(xx , yy , ProbG , levels = lvls , cmap = cm , norm = norm)
            CTF = ax.contourf(xxR , yyR , ProbG_land , levels = lvls , cmap = cm , norm = norm)
            # CT = ax.contour(xxR , yyR , dBZ , levels = lvls_dBZ , colors = 'r' , linewidths = 1)
            SC = ax.scatter(xxRS , yyRS , marker = 'o' , s = 0.1 , c = 'k' , alpha = 0.8 , label = '>= 35 dBZ')
            ax.text(119.8 , 25.60 , model[cnt_m] , fontsize = 6 , ha = 'left' , color = '#888888')
            ax.text(119.8 , 25.45 , 'Probability' , fontsize = 8 , ha = 'left')
            ax.text(122.2 , 25.60 , dtStringLST + ' LST' , fontsize = 8 , ha = 'right')
            ax.text(122.2 , 25.45 , 'Forecast ' + rdtStringLST + ' LST' , fontsize = 8 , ha = 'right')
            leg = ax.legend(loc = 'upper left' , fontsize = 8)
            cb = plt.colorbar(CTF , orientation = 'vertical', ticks = lvls)
            cb.ax.tick_params(labelsize = 6)
            cb.set_label('%' , size = 6 , labelpad = -15 , y = 1.05 , rotation = 0)
            fig.savefig(outPath , dpi = 200)
            print(model[cnt_m] , '-' , dtStringLST + 'L' , '- has been saved!')
