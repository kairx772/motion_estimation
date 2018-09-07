from motion_estimate import optflw as opw
from motion_estimate import visualize as vlz
from motion_estimate import capresize as cpz

x = 6
y = 6
Vx = 1
Vy = 1
n = 60

bp0 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
bp1 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5]
bp2 = [1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8]
bp3 = [1,1,1,2,2,2,2,2,2,3,3,3,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,6,6,6,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]
bp4 = [1,1,2,2,2,2,2,2,3,3,3,3,4,4,4,5,5,5,5,6,6,6,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]
bp5 = [1,1,1,2,2,2,2,3,3,3,3,3,4,4,4,5,5,5,5,5,5,6,6,7,7,7,7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]
bp6 = [1,1,1,2,2,2,2,2,3,3,3,4,4,4,5,5,5,5,5,5,5,6,6,7,7,7,7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]
bp7 = [1,1,1,2,2,2,2,2,3,3,3,4,4,4,5,5,5,5,5,6,6,6,7,7,7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

bp55 = [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]


for Vy in [0,1,2]:
	videoname = 'listdata/circle'
	cpz.GenCirList(videoname, x, y, Vx, Vy, n)
	bkg_bm = 'listdata/circleBMA'
	bkg_bm_fd = 'bkg/BMallspeed/vx'+str(Vx)+'vy'+str(Vy)
	bkg_sal = 'listdata/circleSAL'
	bmcsvname = 'csv/bmvx'+str(Vx)+'vy'+str(Vy)+'.csv'

	opw.GenSallist(videoname, bkg_sal)
	opw.GenBMAdatalist(videoname, bkg_bm)
	vlz.GenCSV(bkg_bm, bkg_sal, bmcsvname)
	#vlz.WriteListToAviwithSalFixP(videoname, bkg_bm_fd, bkg_bm, bkg_sal)
	vlz.WriteListToAviwithSalFixpNetbump(videoname, bkg_bm_fd, bkg_bm, bkg_sal, bp2, bp2)
'''
exportVxy = 'listdata/circleVxy'
exportsal = 'listdata/circlebmsal'
BMloc = 'listdata/circlebmloc'
mbtra_fd = 'bkg/BMtra'
opw.GenBMAdatalistTracing(videoname, exportVxy, BMloc, exportsal, 2, 2)
vlz.WriteListToAviwithSal(videoname, mbtra_fd, exportVxy, exportsal, BMloc)

videoname = 'listdata/sliced_video/pillow_dark_sliced'
exportVxy = 'listdata/circleVxy'
exportsal = 'listdata/circlebmsal'
BMloc = 'listdata/circlebmloc'
mbtra_fd = 'bkg/BMtra'
opw.GenBMAdatalistTracing(videoname, exportVxy, BMloc, exportsal, 48, 56)
vlz.WriteListToAviwithSal(videoname, mbtra_fd, exportVxy, exportsal, BMloc)
'''