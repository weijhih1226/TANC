import os, sys
import glob
import numpy as np
import netCDF4
from netCDF4 import date2num, num2date
from datetime import datetime, timedelta

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
#--------------------------------------------------------------------
# main program
#--------------------------------------------------------------------
fpath_in = './'
filelist = sorted( glob.glob( fpath_in + '/*.nc' ) )
for file_in in filelist:
    try:
        ncfs = netCDF4.Dataset(os.path.join(file_in))
        #print(ncfs)
    except:
        print('Loading ERROR {}'.format(file_in))

    time = ncfs.variables['time']
    date = num2date(time[:], units=time.units)


    lat = np.array(ncfs.variables['latitude'][:])
    lon = np.array(ncfs.variables['longitude'][:])
    var_in = file_in.split('_')[1].split('.')[0]

    if var_in == "tt":
       OUT_str = "TT"
       var = np.array(ncfs.variables['TMP_surface'][:])
       fname_out = f'B00100UKKRH0067600'
    elif var_in == "td":
       OUT_str = "TD"
       var = np.array(ncfs.variables['DPT_surface'][:])
       fname_out = f'B00150UKKRH0067600'
    elif var_in == "uu":
       OUT_str = "UU"
       var = np.array(ncfs.variables['UGRD_surface'][:])
       fname_out = f'B00200RWRFH0067600'
    elif var_in == "vv":
       OUT_str = "VV"
       var = np.array(ncfs.variables['VGRD_surface'][:])
       fname_out = f'B00210RWRFH0067600'
    elif var_in == "wd":
       OUT_str = "WD"
       var = np.array(ncfs.variables['WDIR_surface'][:])
       fname_out = f'B002D0RWRFH0067600'
    elif var_in == "ws":
       OUT_str = "WS"
       var = np.array(ncfs.variables['WIND_surface'][:])
       fname_out = f'B002C0RWRFH0067600'
    ncfs.close()

    for i in range(len(date)) :
        print( date[i].year )
        fpath_out = f'./bin/{OUT_str}/{date[i].year:04d}{date[i].month:02d}{date[i].day:02d}{date[i].hour:02d}000000'

        mk_not_exist_dir( fpath_out )
        output_binfile( fpath_out, fname_out, np.float32(var[i,:,:]) )
