#!/bin/csh

########################################
########### ANC_Checker.csh ############
######## Author: Wei-Jhih Chen #########
########## Update: 2021/12/30 ##########
########################################

echo "---------------- INPUT -----------------"
echo "Year: (ex. 2021)"
set year = $<
echo "Month: (ex. 01)"
set month = `printf "%02d" $<`
echo "Day: (ex. 01)"
set day = `printf "%02d" $<`
set date = $year$month$day
set yr = `date -d $year$month$day +"%y"`
set yday = `date -d $year$month$day +"%j"`
set date_now = `date -u +"%Y%m%d"`
set hour_now = `date -u +"%k"`

set account = "nowcast64"

set RAW_fpath = "/d1/tempdata/nidsB/ancdata"     # raw
set SPDB_fpath = "/home/$account/anc/data/spdb" # spdb
set MDV_fpath = "/home/$account/anc/data/mdv"   # mdv
set LOGISTIC_fpath = "/mnt/ancnas2/logist"

set hour_delay = 1
set hour_vefy_delay = 1
@ hour_end = $hour_now - $hour_delay
@ hour_vefy_end = $hour_end - $hour_vefy_delay
if ( $date == $date_now ) then
    set hours = `seq 0 $hour_end`
    set hours_vefy = `seq 0 $hour_vefy_end`
else
    set hours = `seq 0 23`
    set hours_vefy = `seq 0 23`
endif

@ RAW_fnum = $#hours
@ SPDB_fnum = $#hours
@ MDV_fnum = $#hours
@ LOGISTIC_fnum = $#hours * 6

# RAW data
echo "\n----------------- RAW ------------------"
echo "     ******* STMAS-WRF (WS) *******     "
cd "$RAW_fpath/wrfdata_d01/"
set cnt_Y = `ls wrfout_d01_$year-$month-$day*00 |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "wrfout_d01_$year-$month-$day"_"$hour"00"" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n     ********* RWRF (WS) **********     "
cd "$RAW_fpath/rwrf/"
set cnt_Y = `ls wrfout_d01_$year-$month-$day*00 |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "wrfout_d01_$year-$month-$day"_"$hour"00"" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n     ********* RWRF (MR) **********     "
echo "          **** fua(00).mr ****          "
cd "$RAW_fpath/radar_wrf/fua/"
set cnt_Y = `ls $yr$yday*000000.mr |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$yr$yday$hour"000000".mr" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          **** fua(01).mr ****          "
set cnt_Y = `ls $yr$yday*000100.mr |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$yr$yday$hour"000100".mr" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          **** fua(02).mr ****          "
set cnt_Y = `ls $yr$yday*000200.mr |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$yr$yday$hour"000200".mr" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          *** fua(00).anc ****          "
cd "$RAW_fpath/radar_wrf/fua/"
set cnt_Y = `ls $yr$yday*000000.anc |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$yr$yday$hour"000000".anc" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          *** fua(01).anc ****          "
set cnt_Y = `ls $yr$yday*000100.anc |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$yr$yday$hour"000100".anc" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          *** fua(02).anc ****          "
set cnt_Y = `ls $yr$yday*000200.anc |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$yr$yday$hour"000200".anc" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n     ******* OBS (DIV & LI) *******     "
echo "          ******** QC ********          "
cd "$RAW_fpath/station/QC/"
set cnt_Y = `ls $year$month$day*.QPESUMS_STATION.10M_new.mdf |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$year$month$day$hour$minute.QPESUMS_STATION.10M_new.mdf" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******* 10M ********          "
cd "$RAW_fpath/station/10M/"
set cnt_Y = `ls $year$month$day*.QPESUMS_STATION.10M.mdf |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$year$month$day$hour$minute.QPESUMS_STATION.10M.mdf" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******* 15M ********          "
cd "$RAW_fpath/station/15M/"
set cnt_Y = `ls $year$month$day*.QPESUMS_STATION.15M.mdf |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$year$month$day$hour$minute.QPESUMS_STATION.15M.mdf" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n     ******* SATELLITE (MR) *******     "
echo "          ******** b1 ********          "
cd "$RAW_fpath/satellite/M_HIMA/b1/"
set cnt_Y = `ls $year$month$day-*00.plain |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$year$month$day-$hour$minute"00".plain" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******** b2 ********          "
cd "$RAW_fpath/satellite/M_HIMA/b2/"
set cnt_Y = `ls $year$month$day-*00.plain |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$year$month$day-$hour$minute"00".plain" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******** b3 ********          "
cd "$RAW_fpath/satellite/M_HIMA/b3/"
set cnt_Y = `ls $year$month$day-*00.plain |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$year$month$day-$hour$minute"00".plain" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******** b4 ********          "
cd "$RAW_fpath/satellite/M_HIMA/b4/"
set cnt_Y = `ls $year$month$day-*00.plain |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$year$month$day-$hour$minute"00".plain" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******* sza ********          "
cd "$RAW_fpath/satellite/M_HIMA/sza/"
set cnt_Y = `ls $year$month$day-*00.plain |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$year$month$day-$hour$minute"00".plain" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n     **** RADAR COMPREF MOSAIC ****     "
cd "$RAW_fpath/compref_mosaic/"
set cnt_Y = `ls COMPREF.$year$month$day.*.gz |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "COMPREF.$year$month$day.$hour$minute.gz" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

# SPDB data
echo "\n----------------- SPDB -----------------"
echo "     ******* SOUNDING (OBS) *******     "
cd "$SPDB_fpath/fggeSoundingIngest/"
ll *.data

echo "\n     ****** SOUNDING (FCST) *******     "
echo "          ******* d01 ********          "
cd "$SPDB_fpath/rucSounding/d01/"
ll *.data

echo "\n          ******* rwrf *******          "
cd "$SPDB_fpath/rucSounding/rwrf/f01/"
ll *.data

echo "\n          ***** rwrf_WS ******          "
cd "$SPDB_fpath/rucSounding/rwrf_WS/"
ll *.data

# MDV data
echo "\n----------------- MDV ------------------"
echo "     ******* STMAS-WRF (WS) *******     "
echo "          **** Likelihood ****          "
cd "$MDV_fpath/cronus/init60_d01/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$hour$minute"00".mdv" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******* CAPE *******          "
cd "$MDV_fpath/mdvConvert/cape/d01/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$hour"0000".mdv" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******* CIN ********          "
cd "$MDV_fpath/mdvCinProcess/d01/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$hour"0000".mdv" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******** RH ********          "
cd "$MDV_fpath/verticalAverage/rh/d01/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$hour"0000".mdv" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******* DIV ********          "
cd "$MDV_fpath/surfInterp2/d01/QC/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 5 55`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$hour$minute"00".mdv" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n     ********* RWRF (WS) **********     "
echo "          **** Likelihood ****          "
cd "$MDV_fpath/cronus/init60_rwrf_WS/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$hour$minute"00".mdv" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******* CAPE *******          "
cd "$MDV_fpath/mdvConvert/cape/rwrf_WS/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$hour"0000".mdv" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******* CIN ********          "
cd "$MDV_fpath/mdvCinProcess/rwrf_WS/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$hour"0000".mdv" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******** RH ********          "
cd "$MDV_fpath/verticalAverage/rh/rwrf_WS/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$hour"0000".mdv" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******* DIV ********          "
cd "$MDV_fpath/surfInterp2/rwrf_WS/QC/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 5 55`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$hour$minute"00".mdv" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n     ********* RADAR (WS) *********     "
echo "          ***** Radar Cu *****          "
cd "$MDV_fpath/advectGrid/dbz/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$hour$minute"00".mdv" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          *** StormInitLoc ***          "
cd "$MDV_fpath/stormInitLocs/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$hour$minute"00".mdv" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n     ********* RWRF (MR) **********     "
echo "          **** Likelihood ****          "
cd "$MDV_fpath/cronus/init60_rwrf_MR/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$hour$minute"00".mdv" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******* CAPE *******          "
cd "$MDV_fpath/mdvConvert/rwrf_MR/f01/cape/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$hour"0000".mdv" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******* CIN ********          "
cd "$MDV_fpath/mdvCinProcess/rwrf_MR/f01/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$hour"0000".mdv" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******** RH ********          "
cd "$MDV_fpath/verticalAverage/rwrf_MR/f01/rh/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$hour"0000".mdv" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******** W *********          "
cd "$MDV_fpath/mdvConvert/rwrf_MR/f01/w/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$hour"0000".mdv" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          * Front Likelihood *          "
cd "$MDV_fpath/mitStormFilter/rwrf/f01/fronts/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$hour"0000".mdv" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          * VertSumInterest **          "
cd "$MDV_fpath/vertSumInterest/rwrf/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$hour"0000".mdv" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ******* DIV ********          "
cd "$MDV_fpath/surfInterp2/rwrf_MR/f01/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 5 55`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$hour$minute"00".mdv" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ** Cloud Classify **          "
cd "$MDV_fpath/advectGrid/mdvMultFilt/HIMA8/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$hour$minute"00".mdv" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          ****** IR ROC ******          "
cd "$MDV_fpath/advectGrid/mdvMask/HIMA8.ir10.7/$date/"
set cnt_Y = `ls *00.mdv |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "$hour$minute"00".mdv" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

# Logistic ANC-WS Data
echo "\n--------------- LOGISTIC ---------------"
echo "     *********** ANC-WS ***********     "
echo "          ******* dat ********          "
cd $LOGISTIC_fpath/RWRF_ANC_WS/OUTPUT/
set cnt_Y = `ls $year$month$day/*.dat |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e $year$month$day/$hour$minute"00.dat" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          **** png (fcst) ****          "
cd $LOGISTIC_fpath/RWRF_ANC_WS/
set cnt_Y = `ls $year$month$day/2D_PIC/fcst_logi_*.png |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e $year$month$day/2D_PIC/fcst_logi_$hour$minute.png ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          **** png (vefy) ****          "
cd $LOGISTIC_fpath/RWRF_ANC_WS/
set cnt_Y = `ls $year$month$day/2D_PIC/vefy_logi_*.png |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours_vefy)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e $year$month$day/2D_PIC/vefy_logi_$hour$minute.png ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

# Logistic ANC-MR Data
echo "\n     *********** ANC-MR ***********     "
echo "          ******* dat ********          "
cd $LOGISTIC_fpath/RWRF_ANC_MR/OUTPUT/
set cnt_Y = `ls $year$month$day/*.dat |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e $year$month$day/$hour$minute"00.dat" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          **** png (fcst) ****          "
cd $LOGISTIC_fpath/RWRF_ANC_MR/
set cnt_Y = `ls $year$month$day/2D_PIC/fcst_logi_*.png |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e $year$month$day/2D_PIC/fcst_logi_$hour$minute.png ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif

echo "\n          **** png (vefy) ****          "
cd $LOGISTIC_fpath/RWRF_ANC_MR/
set cnt_Y = `ls $year$month$day/2D_PIC/vefy_logi_*.png |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours_vefy)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e $year$month$day/2D_PIC/vefy_logi_$hour$minute.png ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
    endif
endif
echo "\n----------------- end ------------------"
