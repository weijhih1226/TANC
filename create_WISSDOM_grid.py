import math
import numpy as np

LONC = 119. # Unit: deg
LATC = 21.  # Unit: deg
XMIN = 0.   # Unit: km
XMAX = 409. # Unit: km
YMIN = 0    # Unit: km
YMAX = 559  # Unit: km
ZMIN = 0.   # Unit: km
ZMAX = 4.5  # Unit: km
DX   = 1.   # Unit: km
DY   = 1    # Unit: km
DZ   = 0.5  # Unit: km

XNUM = int((XMAX - XMIN) / DX) + 1
YNUM = int((YMAX - YMIN) / DY) + 1

radius = 6371. # Unit: km
LATDegPerKm = 360 / (2 * radius * np.pi) # Unit: deg
DY_deg = DY * LATDegPerKm # Unit: deg
LON = np.empty((XNUM , YNUM))
LAT = np.empty((XNUM , YNUM))
for cnt_X in range(XNUM):
    for cnt_Y in range(YNUM):
        LAT[cnt_X , cnt_Y] = (YMIN + DY * cnt_Y) * LATDegPerKm + LATC
        LONDegPerKm = 360 / (2 * radius * np.cos(LAT[cnt_X , cnt_Y] / 360 * 2 * np.pi) * np.pi) # Unit: deg
        DX_deg = DX * LONDegPerKm # Unit: deg
        LON[cnt_X , cnt_Y] = (XMIN + DX * cnt_X) * LONDegPerKm + LONC

LON = np.reshape(LON , (XNUM * YNUM , 1))
LAT = np.reshape(LAT , (XNUM * YNUM , 1))
LONLAT = np.hstack((LON , LAT))

with open("ref/WISSDOM_grid.dat" , 'wb') as f:
    f.write(b'Longitude (oE)\tLatitude (oN)\n')
    np.savetxt(f , LONLAT , delimiter = "\t")