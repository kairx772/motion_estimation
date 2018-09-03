import cv2
import numpy as np
import pickle
import cairo
import numpy as np
import csv

winsize = 8

def DrawBox(frame, x, y, r, g, b):
    p = 0
    q = 0
    if x == 56:
        p = 1
    if y == 56:
        q = 1

    frame[x*12,y*12:(y+winsize)*12-q] = [r, g, b]
    frame[x*12+1,y*12:(y+winsize)*12-q] = [r, g, b]
    frame[x*12+2,y*12:(y+winsize)*12-q] = [r, g, b]
    frame[(x+winsize)*12-p,y*12:(y+winsize)*12-q] = [r, g, b]
    frame[(x+winsize)*12-p-1,y*12:(y+winsize)*12-q] = [r, g, b]
    frame[(x+winsize)*12-p-2,y*12:(y+winsize)*12-q] = [r, g, b]
    frame[x*12:(x+winsize)*12-p,y*12] = [r, g, b]
    frame[x*12:(x+winsize)*12-p,y*12+1] = [r, g, b]
    frame[x*12:(x+winsize)*12-p,y*12+2] = [r, g, b]
    frame[x*12:(x+winsize)*12-p,(y+winsize)*12-q] = [r, g, b]
    frame[x*12:(x+winsize)*12-p,(y+winsize)*12-q-1] = [r, g, b]
    frame[x*12:(x+winsize)*12-p,(y+winsize)*12-q-2] = [r, g, b]
    return frame

def DrawboxBig(frame, x, y):
    p = 1
    q = 1

    frame[x*12,y*12:(y+winsize)*12-q] = [0, 0, 255]
    frame[x*12+1,y*12:(y+winsize)*12-q] = [0, 0, 255]
    frame[x*12+2,y*12:(y+winsize)*12-q] = [0, 0, 255]
    frame[(x+winsize)*12-p,y*12:(y+winsize)*12-q] = [0, 0, 255]
    frame[(x+winsize)*12-p-1,y*12:(y+winsize)*12-q] = [0, 0, 255]
    frame[(x+winsize)*12-p-2,y*12:(y+winsize)*12-q] = [0, 0, 255]
    frame[x*12:(x+winsize)*12-p,y*12] = [0, 0, 255]
    frame[x*12:(x+winsize)*12-p,y*12+1] = [0, 0, 255]
    frame[x*12:(x+winsize)*12-p,y*12+2] = [0, 0, 255]
    frame[x*12:(x+winsize)*12-p,(y+winsize)*12-q] = [0, 0, 255]
    frame[x*12:(x+winsize)*12-p,(y+winsize)*12-q-1] = [0, 0, 255]
    frame[x*12:(x+winsize)*12-p,(y+winsize)*12-q-2] = [0, 0, 255]
    return frame


def DrawBoxline(frame, x, y):
    cv2.line(frame,(i*8*12+48,j*8*12+48),(i*8*12+48+parax,j*8*12+48+paray),(255,0,0),5)
    p = 0
    q = 0
    if x == 56:
        p = 1
    if y == 56:
        q = 1
    frame[x*12,y*12:(y+winsize)*12-q] = [0, 0, 255]
    frame[(x+winsize)*12-p,y*12:(y+winsize)*12-q] = [0, 0, 255]
    frame[x*12:(x+winsize)*12-p,y*12] = [0, 0, 255]
    frame[x*12:(x+winsize)*12-p,(y+winsize)*12-q] = [0, 0, 255]
    return frame

def DrawLine(frame):
    for dri in xrange(8):
        frame[dri*8*12, :] = [255, 255, 255]
        frame[:, dri*8*12] = [255, 255, 255]
    return frame

def DrawVxyArrow(frame, x, y, Vx, Vy):
    parax = int(Vx*10)
    paray = int(Vy*10)
    cv2.line(frame,(x*12,y*12),(x*12+parax,y*12+paray),(0,255,0),5)
    cv2.circle(frame,(x*12+parax,y*12+paray), 7, (0,255,0), -1)
    return frame


def GenCSV(vxyname, sallist, exporfoldername):
    with open (vxyname, 'rb') as fp:
        vxydata = pickle.load(fp)
    with open (sallist, 'rb') as fp:
        saldata = pickle.load(fp)
    Vx, Vy = 0,0
    with open(exporfoldername, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['saliency_x', 'saliency_y','Vx' ,'Vy'])
        for i,j in zip(saldata, vxydata):
            Vx = j[i[0],i[1], 0]
            Vy = j[i[0],i[1], 1]
            writer.writerow([str(i[0]+1), str(i[1]+1), str(Vx), str(Vy)])

def GenCSVsalonly(vxysalname, sallist, exporfoldername):
    with open (vxysalname, 'rb') as fp:
        vxydata = pickle.load(fp)
    with open (sallist, 'rb') as fp:
        saldata = pickle.load(fp)
    Vxp, Vxn, Vyp, Vyn = 0,0,0,0
    with open(exporfoldername, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['saliency_x', 'saliency_y','Vx+' ,'Vx-' ,'Vy+' ,'Vy-'])
        for i,j in zip(saldata, vxydata):
            if j[0] > 0:
                Vxp = j[0]
                Vxn = 0
            if j[0] < 0:
                Vxp = 0
                Vxn = -j[0]
            if j[1] > 0:
                Vyp = j[1]
                Vyn = 0
            if j[1] < 0:
                Vyp = 0
                Vyn = -j[1]
            writer.writerow([str(i[0]), str(i[1]), str(Vxp), str(Vxn), str(Vyp), str(Vyn)])

def WriteListToAviwithSal(filmlistfilename, vxyname, sallist, loclist, exporfoldername):
    with open (filmlistfilename, 'rb') as fp:
        listdata = pickle.load(fp)
    with open (vxyname, 'rb') as fp:
        Vxydata = pickle.load(fp)
    with open (sallist, 'rb') as fp:
        saldata = pickle.load(fp)
    with open (loclist, 'rb') as fp:
        locdata = pickle.load(fp)
    n = 0
    for frame, vxy, sal, loc in zip(listdata, Vxydata, saldata, locdata):
        print vxy, sal, loc
        bigimg = np.kron(frame, np.ones((12,12))).astype(np.uint8)
        colorframe = cv2.cvtColor(bigimg, cv2.COLOR_GRAY2RGB)
        colorframe = DrawVxyArrow(colorframe, loc[0]+4, loc[1]+4, vxy[0], vxy[1])
        colorframe = DrawLine(colorframe)
        #colorframe = DrawBox(colorframe, loc[0], loc[1], 0, 255, 0)
        cv2.rectangle(colorframe,(loc[0]*12,loc[1]*12),((loc[0]+8)*12,(loc[1]+8)*12),(0,255,0),5)
        colorframe = DrawBox(colorframe, sal[0]*8, sal[1]*8, 255, 0, 0)
        cv2.imwrite(exporfoldername+'/gray%d.jpg' % n, colorframe)
        n += 1

def WriteListToAviwithSalFixP(filmlistfilename, vxyname, exporfoldername, sallist):
    with open (filmlistfilename, 'rb') as fp:
        listdata = pickle.load(fp)
    with open (vxyname, 'rb') as fp:
        BMAdata = pickle.load(fp)
    with open (sallist, 'rb') as fp:
        saldata = pickle.load(fp)
    btrgb=[]
    for clr in listdata:
        bigimg = np.kron(clr, np.ones((12,12))).astype(np.uint8)
        brgb = cv2.cvtColor(bigimg, cv2.COLOR_GRAY2RGB)
        btrgb.append(brgb)
    n = 0
    for backtorgb, sal in zip(btrgb, saldata):
        
        for i in range(8):
            for j in range(8):
                parax = int(BMAdata[n][j,i,1]*10)
                paray = int(BMAdata[n][j,i,0]*10)
                cv2.line(backtorgb,(i*8*12+48,j*8*12+48),(i*8*12+48+parax,j*8*12+48+paray),(255,0,0),5)
                cv2.circle(backtorgb,(i*8*12+48+parax,j*8*12+48+paray), 7, (255,0,0), -1)
        for dri in xrange(8):
            backtorgb[dri*8*12, :] = [255, 255, 255]
            backtorgb[:, dri*8*12] = [255, 255, 255]
        backtorgb = DrawBox(backtorgb, sal[0]*8, sal[1]*8, 255, 0, 0)
        
        cv2.imwrite(exporfoldername+'/gray%d.jpg' % n, backtorgb)
        n+=1



