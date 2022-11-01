#!/bin/csh

########################################
######### Logistic_Checker.csh #########
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

set GT_fpath = "/d1/tempdata/nidsB/ancdata/GT/realtime.ufs"
set SAT_fpath = "/d1/tempdata/nidsB/ancdata/satellite"
set RADAR_fpath = "/d1/tempdata/data/QPESUMS/grid/cref_smooth_060min"
set MOSAIC_fpath = "/d1/tempdata/data/QPESUMS/grid/mosaicPOS_out"
set MODEL_fpath = "/mnt/ancdata/lapsdata/rwrf/post"
set WISSDOM_fpath = "/d1/tempdata/nidsB/ancdata/wissdom"
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

@ GT_fnum = $#hours
@ SAT_fnum = $#hours * 6
@ RADAR_fnum = $#hours * 6
@ MOSAIC_fnum = $#hours * 6
@ MODEL_fnum = $#hours
@ WISSDOM_fnum = $#hours * 6
@ LOGISTIC_fnum = $#hours * 6

# GT Data
echo "\n------------------ GT ------------------"
echo "          ******** TT ********          "
cd "$GT_fpath/TT/"
set cnt_Y = `ls $year$month$day*000000/B00100UKKRH0067600 |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$year$month$day$hour"000000"/B00100UKKRH0067600" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=108 $year$month$day*000000
    endif
endif

echo "\n          ******** TD ********          "
cd "$GT_fpath/TD/"
set cnt_Y = `ls $year$month$day*000000/B00150UKKRH0067600 |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$year$month$day$hour"000000"/B00150UKKRH0067600" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=108 $year$month$day*000000
    endif
endif

echo "\n          ******** UU ********          "
cd "$GT_fpath/UU/"
set cnt_Y = `ls $year$month$day*000000/B00200RWRFH0067600 |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$year$month$day$hour"000000"/B00200RWRFH0067600" ) then
            @ cnt_N += 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=108 $year$month$day*000000
    endif
endif

echo "\n          ******** VV ********          "
cd "$GT_fpath/VV/"
set cnt_Y = `ls $year$month$day*000000/B00210RWRFH0067600 |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$year$month$day$hour"000000"/B00210RWRFH0067600" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=108 $year$month$day*000000
    endif
endif

echo "\n          ******** WD ********          "
cd "$GT_fpath/WD/"
set cnt_Y = `ls $year$month$day*000000/B002D0RWRFH0067600 |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$year$month$day$hour"000000"/B002D0RWRFH0067600" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=108 $year$month$day*000000
    endif
endif

echo "\n          ******** WS ********          "
cd "$GT_fpath/WS/"
set cnt_Y = `ls $year$month$day*000000/B002C0RWRFH0067600 |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$year$month$day$hour"000000"/B002C0RWRFH0067600" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=108 $year$month$day*000000
    endif
endif

# SAT Data
echo "\n----------------- SAT ------------------"
cd "$SAT_fpath/CLAVRx/"
set cnt_Y = `ls clavrx_H08_$year$month$day*_anc.level2.nc |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "clavrx_H08_$year$month$day"_"$hour$minute"_"anc.level2.nc" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=120 clavrx_H08_$year$month$day*_anc.level2.nc
    endif
endif

# RADAR Data
echo "\n---------------- RADAR -----------------"
cd "$RADAR_fpath/"
set cnt_Y = `ls cref_smooth_060min.$year$month$day* |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "cref_smooth_060min.$year$month$day.$hour$minute" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=102 cref_smooth_060min.$year$month$day*
    endif
endif

# MOSAIC Data
echo "\n---------------- MOSAIC ----------------"
cd "$MOSAIC_fpath/"
set cnt_Y = `ls mosaicPOS_$year$month$day*.dat |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "mosaicPOS_$year$month$day$hour$minute.dat" ) then
                @ cnt_N = $cnt_N + 1
                echo "            $year/$month/$day $hour":"$minute            "
            endif
        end
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=84 mosaicPOS_$year$month$day*.dat
    endif
endif

# MODEL Data
echo "\n---------------- MODEL -----------------"
echo "          ***** fua(00) ******          "
cd "$MODEL_fpath/fua/"
set cnt_Y = `ls -l $year-$month-$day*/$yr$yday*000000.fua |grep "^-" |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$year-$month-$day"_"$hour/$yr$yday$hour"000000".fua" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=90 $year-$month-$day*
    endif
endif

echo "\n          ***** fua(01) ******          "
set cnt_Y = `ls -l $year-$month-$day*/$yr$yday*000100.fua |grep "^-" |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$year-$month-$day"_"$hour/$yr$yday$hour"000100".fua" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=90 $year-$month-$day*
    endif
endif

echo "\n          ***** fua(02) ******          "
set cnt_Y = `ls -l $year-$month-$day*/$yr$yday*000200.fua |grep "^-" |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$year-$month-$day"_"$hour/$yr$yday$hour"000200".fua" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=90 $year-$month-$day*
    endif
endif

echo "\n          ***** fua(03) ******          "
set cnt_Y = `ls -l $year-$month-$day*/$yr$yday*000300.fua |grep "^-" |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$year-$month-$day"_"$hour/$yr$yday$hour"000300".fua" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=90 $year-$month-$day*
    endif
endif

echo "\n          ***** fsf(00) ******          "
cd "$MODEL_fpath/fsf/"
set cnt_Y = `ls -l $year-$month-$day*/$yr$yday*000000.fsf |grep "^-" |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$year-$month-$day"_"$hour/$yr$yday$hour"000000".fsf" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=90 $year-$month-$day*
    endif
endif

echo "\n          ***** fsf(01) ******          "
set cnt_Y = `ls -l $year-$month-$day*/$yr$yday*000100.fsf |grep "^-" |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$year-$month-$day"_"$hour/$yr$yday$hour"000100".fsf" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=90 $year-$month-$day*
    endif
endif

echo "\n          ***** fsf(02) ******          "
set cnt_Y = `ls -l $year-$month-$day*/$yr$yday*000200.fsf |grep "^-" |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$year-$month-$day"_"$hour/$yr$yday$hour"000200".fsf" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=90 $year-$month-$day*
    endif
endif

echo "\n          ***** fsf(03) ******          "
set cnt_Y = `ls -l $year-$month-$day*/$yr$yday*000300.fsf |grep "^-" |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        if ( ! -e "$year-$month-$day"_"$hour/$yr$yday$hour"000300".fsf" ) then
            @ cnt_N = $cnt_N + 1
            echo "            $year/$month/$day $hour            "
        endif
    end
    if ( $cnt_N == 0 ) then
        echo "         All Files were Found!          "
    else
        echo "         $cnt_N File(s) Not Found!          "
        # ls -dx --w=90 $year-$month-$day*
    endif
endif

# WISSDOM Data
echo "\n--------------- WISSDOM ----------------"
echo "          ******* bin ********          "
cd "$WISSDOM_fpath"
set cnt_Y = `ls wissdom_out_$year$month$day*.bin |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "wissdom_out_$year$month$day"_"$hour$minute"_"9.6.2.bin" && ! -e "wissdom_out_$year$month$day"_"$hour$minute"_"source.bin" ) then
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

echo "\n          ******* ctl ********          "
cd "$WISSDOM_fpath"
set cnt_Y = `ls wissdom_out_$year$month$day*.ctl |wc -l`
if ( $cnt_Y == 0 ) then
    echo "               NO Files!                "
else
    set cnt_N = 0
    foreach cnt_hour ($hours)
        set hour = `printf "%02d" $cnt_hour`
        foreach cnt_minute (`seq 0 10 50`)
            set minute = `printf "%02d" $cnt_minute`
            if ( ! -e "wissdom_out_$year$month$day"_"$hour$minute"_"9.6.2.ctl" && ! -e "wissdom_out_$year$month$day"_"$hour$minute"_"source.ctl" ) then
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

# Logistic RAW Data
echo "\n--------------- LOGISTIC ---------------"
echo "     ************ RAW *************     "
echo "          ******* dat ********          "
cd $LOGISTIC_fpath/RWRF_NO_ANC_WS/OUTPUT/
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
cd $LOGISTIC_fpath/RWRF_NO_ANC_WS/
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
cd $LOGISTIC_fpath/RWRF_NO_ANC_WS/
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

# Logistic RAW (WISSDOM) Data
echo "\n     ******* RAW (WISSDOM) ********     "
echo "          ******* dat ********          "
cd $LOGISTIC_fpath/RWRF_NO_ANC_WS_WISS/OUTPUT/
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
cd $LOGISTIC_fpath/RWRF_NO_ANC_WS_WISS/
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
cd $LOGISTIC_fpath/RWRF_NO_ANC_WS_WISS/
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
