import cv2
import numpy as np
import pickle
import cairo
import numpy as np
import csv

winsize = 8

def DrawBox(frame, x, y, r, g, b, w):
    cv2.rectangle(frame,(y*12,x*12),((y+8)*12,(x+8)*12),(r,g,b),w)
    return frame

def DrawLine(frame):
    for dri in xrange(8):
        frame[dri*8*12, :] = [255, 255, 255]
        frame[:, dri*8*12] = [255, 255, 255]
    return frame

def DrawVxyArrow(frame, x, y, Vx, Vy, r, g, b):
    parax = int(Vx*10)
    paray = int(Vy*10)
    cv2.line(frame,(x*12,y*12),(x*12+parax,y*12+paray),(r, g, b),5)
    cv2.circle(frame,(x*12+parax,y*12+paray), 7, (r, g, b), -1)
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

def WriteListToAviwithSal(filmlistfilename, exporfoldername, vxyname, sallist, loclist):
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
        colorframe = DrawVxyArrow(colorframe, loc[1]+4, loc[0]+4, vxy[1], vxy[0], 0, 255, 0)
        #DrawVxyArrow(colorframe, loc[0]+4, loc[1]*8+4, int(vxy[0]), int(vxy[1]), 255, 0, 0)
        colorframe = DrawLine(colorframe)
        #colorframe = DrawBox(colorframe, loc[0], loc[1], 0, 255, 0)
        #cv2.rectangle(colorframe,(loc[0]*12,loc[1]*12),((loc[0]+8)*12,(loc[1]+8)*12),(0,255,0),5)
        colorframe = DrawBox(colorframe, loc[0], loc[1], 0, 255, 0)
        colorframe = DrawBox(colorframe, sal[0]*8, sal[1]*8, 255, 0, 0)
        cv2.imwrite(exporfoldername+'/gray%d.jpg' % n, colorframe)
        n += 1

def WriteListToAviwithSalFixP(filmlistfilename, exporfoldername, vxyname, sallist):
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
                parax = int(BMAdata[n][j,i,1])
                paray = int(BMAdata[n][j,i,0])
                DrawVxyArrow(backtorgb, i*8+4, j*8+4, parax, paray, 255, 0, 0)
        for dri in xrange(8):
            backtorgb[dri*8*12, :] = [255, 255, 255]
            backtorgb[:, dri*8*12] = [255, 255, 255]
        backtorgb = DrawBox(backtorgb, sal[0]*8, sal[1]*8, 255, 0, 0, 3)
        cv2.imwrite(exporfoldername+'/gray%d.jpg' % n, backtorgb)
        n+=1

def WriteListToAviwithSalFixpNetbump(filmlistfilename, 
                                     exporfoldername, 
                                     vxyname, 
                                     sallist, 
                                     neuronnumber0, 
                                     neuronnumber1):
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
    for backtorgb, sal, bpx, bpy in zip(btrgb, saldata, neuronnumber0, neuronnumber1):
        for i in range(8):
            for j in range(8):
                parax = int(BMAdata[n][j,i,1])
                paray = int(BMAdata[n][j,i,0])
                DrawVxyArrow(backtorgb, i*8+4, j*8+4, parax, paray, 255, 0, 0)
        for dri in xrange(8):
            backtorgb[dri*8*12, :] = [255, 255, 255]
            backtorgb[:, dri*8*12] = [255, 255, 255]
        backtorgb = DrawBox(backtorgb, (bpx-1)*8, (bpy-1)*8, 0, 255, 0, 7)
        backtorgb = DrawBox(backtorgb, sal[0]*8, sal[1]*8, 255, 0, 0, 2)
        cv2.imwrite(exporfoldername+'/gray%d.jpg' % n, backtorgb)
        n+=1