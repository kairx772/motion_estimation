import numpy as np
import pickle
import math
import numpy as np
from scipy import ndimage
import itertools
import csv

# block size
winsize = 8

def Compute_Centroid(im1, im2):
    uv = np.zeros((8,8,2))
    # within window window_size * window_size
    for i in range(0, 8):
        for j in range(0, 8):
            ced1 = ndimage.measurements.center_of_mass(im1[i*8:i*8+8, j*8:j*8+8])
            ced2 = ndimage.measurements.center_of_mass(im2[i*8:i*8+8, j*8:j*8+8])
            nu = [ced2[0] - ced1[0],ced2[1] - ced1[1]]
            if math.isnan(nu[0]) or math.isnan(nu[1]):
                uv[i,j,0]=0
                uv[i,j,1]=0
            else:
                uv[i,j,0]=nu[0]
                uv[i,j,1]=nu[1]
    return uv

def BMAvelocity(x, y, prevfm, nextfm):
    bestVxy = [0, 0]
    bestcost = 99999
    if x ==56:
        xwinmax = 0
    if y ==56:
        ywinmax = 0
    if x ==0:
        xwinmin = 0
    if y ==0:
        ywinmin = 0
    for Wx in [4, -4, 3, -3, 2, -2, 1, -1, 0]:
        for Wy in [4, -4, 3, -3, 2, -2, 1, -1, 0]:
            srchx, srchy = x+Wx, y+Wy
            if srchx<0:
                srchx = 0
            if srchx>56:
                srchx = 56
            if srchy<0:
                srchy = 0
            if srchy>56:
                srchy = 56
            cost = np.sum(np.absolute(np.subtract(prevfm[x:x+winsize,y:y+winsize].astype(int),nextfm[srchx:srchx+winsize,srchy:srchy+winsize].astype(int))))
            if cost <= bestcost:
                bestcost = cost
                bestVxy = [srchx-x,srchy-y]
    return bestVxy

def FindMatchBlock(x, y, prevfm, nextfm, winmin, winmax):
    bestxy = [x, y]
    bestcost = 99999
    if x ==56:
        xwinmax = 0
    if y ==56:
        ywinmax = 0
    for Wx in [4, -4, 3, -3, 2, -2, 1, -1, 0]: #xrange(xwinmin, xwinmax)
        for Wy in [4, -4, 3, -3, 2, -2, 1, -1, 0]: #xrange(ywinmin, ywinmax)
            srchx, srchy = x+Wx, y+Wy
            #srchx = clamp(srchx, 0, 64 - winsize -1)
            #srchy = clamp(srchy, 0, 64 - winsize -1)
            #calculate SAD
            cost = np.sum(np.absolute(np.subtract(prevfm[x:x+winsize,y:y+winsize].astype(int),nextfm[srchx:srchx+winsize,srchy:srchy+winsize].astype(int))))
            #compare and find smallest SAD
            if cost < bestcost:
                bestcost = cost
                bestxy = [srchx,srchy]
    #print bestxy
    return bestxy

def Diff_frame(frame1, frame2):
    Diff = 128 + (frame1//2).astype(np.int8) - (frame2//2).astype(np.int8)
    return Diff

def CompressFrame(Diff):
    Loc = np.zeros((8, 8))
    for i,j in itertools.product(range(8), range(8)):
        Loc[i][j] = np.sum(Diff[i*8:i*8+8,j*8:j*8+8])/64
    return Loc

def Show_Saliency(frame1, frame2):
    sal_index = [0,0]
    diff = Diff_frame(frame1, frame2)
    box = CompressFrame(diff)
    i,j = np.unravel_index(box.argmax(), box.shape)
    sal_index = [i,j]
    return sal_index

def GenSallist(listfilename, exportfilename):
    with open (listfilename, 'rb') as fp:
        listdata = pickle.load(fp)
    datalist = []
    sal_data = [0,0]
    nextfm = listdata[0]
    prevfm = listdata[0]
    n = 0
    for k in listdata:
        nextfm = k
        datalist.append(Show_Saliency(nextfm, prevfm))
        prevfm = k
        n += 1
    with open(exportfilename, 'wb') as fp:
        pickle.dump(datalist, fp)

def GenLKdatalist(listfilename, exportfilename):
    with open (listfilename, 'rb') as fp:
        listdata = pickle.load(fp)
    LKdatalist = []
    LKdata = np.zeros((8,8,2))
    nextfm = listdata[0]
    prevfm = listdata[0]
    n = 0
    for k in listdata:
        nextfm = k
        LKdatalist.append(optical_flow(nextfm, prevfm))
        prevfm = k
        n += 1
    with open(exportfilename, 'wb') as fp:
        pickle.dump(LKdatalist, fp)

def GenCENdatalist(listfilename, exportfilename):
    with open (listfilename, 'rb') as fp:
        listdata = pickle.load(fp)
    LKdatalist = []
    LKdata = np.zeros((8,8,2))
    nextfm = listdata[0]
    prevfm = listdata[0]
    binary_mass = np.zeros_like(Diff_frame(nextfm, prevfm))
    binary_mass_prev = np.zeros_like(Diff_frame(nextfm, prevfm))
    n = 0
    for k in listdata:
        nextfm = k
        Loc_s = Diff_frame(nextfm, prevfm)
        binary_mass = np.where(Loc_s > 128 + 20, 1, 0)

        LKdata = Compute_Centroid(binary_mass_prev, binary_mass)
        LKdatalist.append(LKdata)
        binary_mass_prev = binary_mass
        prevfm = k
        n += 1
    with open(exportfilename, 'wb') as fp:
        pickle.dump(LKdatalist, fp)


def GenBMAdatalistTracing(listfilename, exportVxy, exportMathcxy, exportsal, inix, iniy):
    with open (listfilename, 'rb') as fp:
        listdata = pickle.load(fp)
    bestxy = [inix, iniy]
    loclist = []
    Vxylist = []
    sal_indexlist = []
    nextfm = listdata[0]
    prevfm = listdata[0]
    n = 0
    for k in listdata:
        nextfm = k
        bestVxy = BMAvelocity(bestxy[0], bestxy[1], prevfm, nextfm)
        bestxy[0] = bestxy[0] + bestVxy[0]
        bestxy[1] = bestxy[1] + bestVxy[1]
        loclist.append([bestxy[0] - bestVxy[0], bestxy[1] - bestVxy[1]])
        
        Vxylist.append(bestVxy)
        sal_indexlist.append([(bestxy[0]+4)//8, (bestxy[1]+4)//8])
        prevfm = k
        bestVxy = [] 
        n += 1
    print Vxylist
    with open(exportVxy, 'wb') as fp:
        pickle.dump(Vxylist, fp)
    with open(exportMathcxy, 'wb') as fp:
        pickle.dump(loclist, fp)
    with open(exportsal, 'wb') as fp:
        pickle.dump(sal_indexlist, fp)

def GenBMAdatalistTracingB(listfilename, exportVxy, exportMathcxy, exportsal, inix, iniy):
    with open (listfilename, 'rb') as fp:
        listdata = pickle.load(fp)
    bestxy = [inix, iniy]
    loclist = []
    Vxylist = []
    sal_indexlist = []
    nextfm = listdata[0]
    prevfm = listdata[0]
    n = 0

    for k in listdata:
        nextfm = k
        bestxy = FindMatchBlock(bestxy[0], bestxy[1], prevfm, nextfm)
        loclist.append([bestxy[0] + bestVxy[0], bestxy[1] + bestVxy[1]])
        
        Vxylist.append(bestVxy)
        sal_indexlist.append([(bestxy[0]+4)//8, (bestxy[1]+4)//8])
        prevfm = k
        bestVxy = [] 
        n += 1
    print Vxylist
    with open(exportVxy, 'wb') as fp:
        pickle.dump(Vxylist, fp)
    with open(exportMathcxy, 'wb') as fp:
        pickle.dump(loclist, fp)
    with open(exportsal, 'wb') as fp:
        pickle.dump(sal_indexlist, fp)

def GenBMAdatalist(listfilename, exportfilename):
    with open (listfilename, 'rb') as fp:
        listdata = pickle.load(fp)
    BMAdatalist = []
    BMAdata = np.zeros((8,8,2))
    nextfm = listdata[0]
    prevfm = listdata[0]
    n = 0
    for k in listdata:
        BMAdata = np.zeros((8,8,2))
        nextfm = k
        for boxi in range(8):
            for boxj in range(8):
                bestVxy = BMAvelocity(boxi*8, boxj*8, prevfm, nextfm) 
                BMAdata[boxi,boxj,0] = bestVxy[0]
                BMAdata[boxi,boxj,1] = bestVxy[1]
        BMAdatalist.append(BMAdata)
        prevfm = k
        n += 1
    with open(exportfilename, 'wb') as fp:
        pickle.dump(BMAdatalist, fp)