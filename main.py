from motion_estimate import optflw as opw
from motion_estimate import visualize as vlz
from motion_estimate import capresize as cpz

x = 6
y = 6
Vx = 1
Vy = 2
n = 60
'''
videoname = 'listdata/circle'
cpz.GenCirList(videoname, x, y, Vx, Vy, n)
bkg_bm = 'listdata/circleBMA'
bkg_cen = 'listdata/circleCEN'
bkg_loc = 'listdata/pikaLoc'
bkg_cen_fd = 'bkg/CEN'
bkg_bm_fd = 'bkg/BM'

bkg_sal = 'listdata/circleSAL'

bmcsvname = 'bm.csv'
cencsvname = 'cen.csv'

opw.GenSallist(videoname, bkg_sal)
opw.GenBMAdatalist(videoname, bkg_bm)
opw.GenCENdatalist(videoname, bkg_cen)
vlz.GenCSV(bkg_bm, bkg_sal, bmcsvname)
vlz.GenCSV(bkg_cen, bkg_sal, cencsvname)


vlz.WriteListToAviwithSalFixP(videoname, bkg_cen_fd, bkg_cen, bkg_sal)
vlz.WriteListToAviwithSalFixP(videoname, bkg_bm_fd, bkg_bm, bkg_sal)


exportVxy = 'listdata/circleVxy'
exportsal = 'listdata/circlebmsal'
BMloc = 'listdata/circlebmloc'
mbtra_fd = 'bkg/BMtra'
opw.GenBMAdatalistTracing(videoname, exportVxy, BMloc, exportsal, 2, 2)
vlz.WriteListToAviwithSal(videoname, mbtra_fd, exportVxy, exportsal, BMloc)
'''
videoname = 'listdata/sliced_video/pillow_dark_sliced'
exportVxy = 'listdata/circleVxy'
exportsal = 'listdata/circlebmsal'
BMloc = 'listdata/circlebmloc'
mbtra_fd = 'bkg/BMtra'
opw.GenBMAdatalistTracing(videoname, exportVxy, BMloc, exportsal, 48, 56)
vlz.WriteListToAviwithSal(videoname, mbtra_fd, exportVxy, exportsal, BMloc)