#!/usr/local/bin/python3

import math
import sys
import numpy as np
import Pre_Oline_Prob_Calibration as popc
from datetime import datetime as dt
from datetime import timedelta as td

case_year = '2021'
case_date = ['0510' , '0513' , '0519' , '0523' , '0609' , '0610' , '0611' , '0612' , '0703' , '0708' , '0709' , '0711' , '0718' , '0729' , '0811' , '0814' , '0815' , '0816' , '0820' , '0821' , '0824' , '0825' , '0826' , '0827']

stime = dt.now()

work_path = '/home/xb112/PreOnline_Calibration/'
ref_path = f'{work_path}/REF/'
InputPath4Obs = '/mnt/mdlanc/nc/stratiform_filter/'

WS_dBz = 35
Grid_Info = '5_group_Kmeans_labels_smooth.dat'

if "-ANC_WS_LH" in sys.argv:
    InputPath4Fcst = '/mnt/logistic/rwrf-WS/OUTPUT/'
    OutputPath = '/home/cwj/Tools/output/logistic/rwrf-WS/'
    BT_DAT = "ANC_BestThreshold.dat"
    title_string = 'Likelihood ANC_WS'
    print( " Verify rwrf-WS !" )
elif "-ANC_WS" in sys.argv:
    InputPath4Fcst = '/mnt/logistic/RWRF_ANC_WS/OUTPUT/'
    OutputPath = '/home/cwj/Tools/output/logistic/RWRF_ANC_WS/'
    BT_DAT = "ANC_WS_BestThreshold.dat"
    title_string = 'Logistic ANC_WS'
    print( " Verify ANC_WS !" )
elif "-NO_ANC_WS" in sys.argv:
    InputPath4Fcst = '/mnt/logistic/RWRF_NO_ANC_WS/OUTPUT/'
    OutputPath = '/home/cwj/Tools/output/logistic/RWRF_NO_ANC_WS/'
    BT_DAT = "NO_ANC_WS_BestThreshold_revised.dat"
    title_string = 'Logistic NO_ANC_WS'
    print( " Verify NO_ANC_WS !" )

lat = popc.readtxt_col( ref_path, Grid_Info, 2 )
lat = lat.astype(np.float32)
lon = popc.readtxt_col( ref_path, Grid_Info, 3 )
lon = lon.astype(np.float32)
group = popc.readtxt_col( ref_path, Grid_Info, 5 )
group = group.astype(np.float32)
group = group.astype(np.int32)
grouplist = ['Taipei','Tao-Chu','Coastal','SouthWest','Mountain','Taiwan']
dashlist = ['-','-','-','-','-','-']
markerlist = ['o','^','s','P','x','d']
dBz_Threshold = WS_dBz
Best_Threshold = popc.readtxt_col( ref_path, BT_DAT, 1 )
Best_Threshold = Best_Threshold.astype(np.float32)

if "-CASE" in sys.argv:
    case_list = str(sys.argv[sys.argv.index("-CASE") + 1])
    time_list = popc.readtxt_col("./",case_list,1)
    verify_list = []
    for i in time_list :
        verify_list.append(dt.strptime( i, "%Y%m%d%H%M") - td(hours=8))
elif "-INTERVAL" in sys.argv:
    sdate = str(sys.argv[sys.argv.index("-INTERVAL") + 1])
    edate = str(sys.argv[sys.argv.index("-INTERVAL") + 2])

if "-CASE" in sys.argv:
    popc.Process_contingency_tables( Best_Threshold, group, verify_list, InputPath4Fcst, InputPath4Obs, ref_path, OutputPath, grouplist, dashlist, markerlist, dBz_Threshold, title_string )
elif( sys.argv[1] in ['-INTERVAL'] ):
    for cnt_c in range(0 , len(case_date)):
        sdt = dt(int(case_year) , int(case_date[cnt_c][0 : 2]) , int(case_date[cnt_c][2 : 4]) , int(sdate[0 : 2]) , int(sdate[2 : 4]) , 0) - td(hours=8) # UTC
        edt = dt(int(case_year) , int(case_date[cnt_c][0 : 2]) , int(case_date[cnt_c][2 : 4]) , int(edate[0 : 2]) , int(edate[2 : 4]) , 0) - td(hours=8) # UTC
        # sdt = dt.strptime(sdate, "%Y%m%d%H%M") - td(hours=8) #  UTC
        # edt = dt.strptime(edate, "%Y%m%d%H%M") - td(hours=8) #  UTC
        sYear = sdt.timetuple()[0] # start year
        eYear = edt.timetuple()[0] # end year
        nYear = edt.timetuple()[0] - sdt.timetuple()[0] + 1 # total years

        TxMM = ["00", "10", "20", "30", "40", "50"]
        if str(int(int(sdate) - math.floor(int(sdate) / 10**2) * 10**2)).zfill(2) not in TxMM:
            print("reset MM of yyyymmddHHMM for Temp")
        verify_list = []
        nDate = 0
        dtobj = sdt

        while dtobj < edt:
            if nDate == 0 :
                verify_list.append( dtobj )
            nDate = nDate + 1
            dtobj = dtobj + td(minutes=10)
            verify_list.append( dtobj )

        popc.Process_contingency_tables( Best_Threshold, group, verify_list, InputPath4Fcst, InputPath4Obs, ref_path, OutputPath, grouplist, dashlist, markerlist, dBz_Threshold, title_string )

etime = dt.now()
print(">>> Exetime: ", str(etime - stime))