import datetime as dt
import netCDF4 as nc
import numpy as np
import os
import matplotlib
#matplotlib.use('AGG')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from datetime import datetime as dtdt
from matplotlib.colors import LinearSegmentedColormap

def mk_not_exist_dir(path):
    try:
        if (not os.path.exists(path)):
             os.makedirs(path)
    except OSError as tmp:
        print(tmp)

def output_binfile(fpath,fname,var):
    with open(fpath+'/'+fname,'w+b') as fid:
        fid.write(var.tobytes('C'))
    fid.close()
def readtxt_col(fpath,fname,col):
    array = np.loadtxt(os.path.join(fpath,fname),usecols=(col-1,),dtype='int')
    return array
def readtxt_col2(fpath,fname,col):
    array = np.loadtxt(os.path.join(fpath,fname),usecols=(col-1,),dtype='float')
    return array
#--------------------------------------------------------------------
# main program
#--------------------------------------------------------------------
date_time_start = dtdt(2021 , 5 , 1 , 0 , 0 , 0) # UTC
date_time_end = dtdt(2021 , 9 , 2 , 23 , 50 , 0) # UTC

timestamp_start = date_time_start.timestamp()
timestamp_end = date_time_end.timestamp()
timestep = 10 # Unit: Minute
time_lag = 1 # Default (Unit: hours)

dir_in = os.listdir('/mnt/mdlanc/nc/rwrf-WS/Init60/')

land_lat = readtxt_col2( '/home/cwj/Tools/ref/', '5_group_Kmeans_labels_smooth.dat', 2 )
land_lon = readtxt_col2( '/home/cwj/Tools/ref/', '5_group_Kmeans_labels_smooth.dat', 3 )
land_x = readtxt_col( '/home/cwj/Tools/ref/', '5_group_Kmeans_labels_smooth.dat', 6 )-1
land_y = readtxt_col( '/home/cwj/Tools/ref/', '5_group_Kmeans_labels_smooth.dat', 7 )-1

# for i in dir_in:
#     name_in = os.listdir('/mnt/mdlanc/nc/rwrf-WS/Init60/'+ i )
#     for j in name_in:
#         if( '.nc' in j ):
#             print('/mnt/mdlanc/nc/rwrf-WS/Init60/',i,j )
#             fpath_in = '/mnt/mdlanc/nc/rwrf-WS/Init60/'+i+'/'
#             try:
#                 ncfs = nc.Dataset(os.path.join(fpath_in,j))
#             except OSError:
#                 continue
#             lon = np.array(ncfs.variables['x0'][:])
#             lat = np.array(ncfs.variables['y0'][:])
#             lon_2d, lat_2d = np.meshgrid( lon, lat )
#             var = np.array(ncfs.variables['Init60_rwrf_WS'][:])
#             ncfs.close()
#             var_2d = var.reshape( len(lat), len(lon) )
#             var_out = var_2d[land_y,land_x]

#             fname_out = j[9:15] + '.dat'

#             fpath_out = '/mnt/logistic/rwrf-WS/OUTPUT/'+i+'/'
#             mk_not_exist_dir(fpath_out)
#             np.savetxt(fpath_out+fname_out,var_out,fmt='%20.10f')

home_inDir = '/mnt/mdlanc/nc/rwrf-WS/Init60/'
home_outDir = '/mnt/logistic/rwrf-WS/OUTPUT/'

for timestamp in np.arange(timestamp_start , timestamp_end + 1 , timestep * 60):
    ##### Set Date/Time #####
    Year =      int(dtdt.fromtimestamp(timestamp).strftime("%Y"))
    Month =     int(dtdt.fromtimestamp(timestamp).strftime("%m"))
    Day =       int(dtdt.fromtimestamp(timestamp).strftime("%d"))
    Hour =      int(dtdt.fromtimestamp(timestamp).strftime("%H"))
    Minute =    int(dtdt.fromtimestamp(timestamp).strftime("%M"))
    Second =    int(dtdt.fromtimestamp(timestamp).strftime("%S"))

    date_time = dtdt(Year , Month , Day , Hour , Minute , Second)
    date_timeLST = date_time + dt.timedelta(hours = 8)

    dateStringUTC = date_time.strftime("%Y%m%d")
    timeStringUTC = date_time.strftime("%H%M%S")
    dtStringLST = date_timeLST.strftime("%Y/%m/%d %H:%M")

    filedate = dateStringUTC
    filetime = timeStringUTC

    ##### Set Path #####
    inPath = home_inDir + filedate + '/' + filedate + '_' + filetime + '.nc'
    outDir = home_outDir + filedate + '/'
    outPath = outDir + filetime + '.dat'
    
    # Create Directory & Skip No File
    if not(os.path.isdir(outDir)):
        os.mkdir(outDir)
        print ("Successfully created the directory %s " % outDir)
    if not(os.path.isfile(inPath)):
        print('No File:' , inPath)
        continue

    ##### Read Radar #####
    try:
        ncfs = nc.Dataset(inPath)
    except OSError:
        continue

    lon = np.array(ncfs.variables['x0'][:])
    lat = np.array(ncfs.variables['y0'][:])
    lon_2d, lat_2d = np.meshgrid( lon, lat )
    var = np.array(ncfs.variables['Init60_rwrf_WS'][:])
    ncfs.close()
    var_2d = var.reshape( len(lat), len(lon) )
    var_out = var_2d[land_y,land_x]

    np.savetxt(outPath , var_out , fmt='%20.10f')
    print(dtStringLST + 'L' , '- has been saved!')