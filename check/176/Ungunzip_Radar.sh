#!/bin/bash

gunzip -d /d1/tempdata/data/QPESUMS/grid/cref_smooth_060min/*.gz
chmod 777 /d1/tempdata/data/QPESUMS/grid/cref_smooth_060min/*
find /d1/tempdata/data/QPESUMS/grid/cref_smooth_060min/ -mtime +7 |xargs rm -f
find /d1/tempdata/data/QPESUMS/grid/mosaicPOS_out/ -mtime +7 |xargs rm -f
