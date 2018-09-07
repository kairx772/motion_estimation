from motion_estimate import optflw as opw
from motion_estimate import visualize as vlz
from motion_estimate import capresize as cpz

videoname = 'listdata/pillow'

bkg_bm = 'listdata/pillowBMA'
bkg_cen = 'listdata/pillowCEN'
bkg_loc = 'listdata/pilowLoc'
bkg_cen_fd = 'bkg/CENpillow'
bkg_bm_fd = 'bkg/BMpillow'

bkg_sal = 'listdata/circleSAL'
#cencsvname = 'csv/cenvx'+str(u)+'vy'+str(v)+'.csv'
#bmcsvname = 'csv/bmvx'+str(u)+'vy'+str(v)+'.csv'

bmcsvname = 'bkg/BMpillow/bm.csv'
cencsvname = 'bkg/CENpillow/cen.csv'

cpz.CaptureVideoTo6464('pillow_bright.mp4', videoname)

opw.GenSallist(videoname, bkg_sal)
opw.GenBMAdatalist(videoname, bkg_bm)
opw.GenCENdatalist(videoname, bkg_cen)
vlz.GenCSV(bkg_bm, bkg_sal, bmcsvname)
vlz.GenCSV(bkg_cen, bkg_sal, cencsvname)


vlz.WriteListToAviwithSalFixP(videoname, bkg_cen_fd, bkg_cen, bkg_sal)
vlz.WriteListToAviwithSalFixP(videoname, bkg_bm_fd, bkg_bm, bkg_sal)