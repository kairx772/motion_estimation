import cv2
import numpy as np
import pickle
import os
import errno
import cairo
import math

def CaptureVideoTo6464(videofilename, exportfilename):
    #print videofilename
    cap = cv2.VideoCapture(videofilename)
    success,image = cap.read()
    count = 0
    success = True
    framelist1 = []
    while success:
        success,image = cap.read()
        if success == True:
            height, width = image.shape[:2]
            rectan = cv2.resize(image, (height,height))
            smallim = cv2.resize(rectan, (64,64))
            gray = cv2.cvtColor(smallim,cv2.COLOR_BGR2GRAY)
            framelist1.append(gray)
        count += 1
    with open(exportfilename, 'wb') as fp:
        pickle.dump(framelist1, fp)
    cap.release()

def ConverToGrayFrame(listfilename, grayfoldername):
    with open (listfilename, 'rb') as fp:
        listdata = pickle.load(fp)
    try:
        os.makedirs(grayfoldername)
    except OSError, e:
        if e.errno != os.errno.EEXIST:
            raise
    n = 0
    for k in listdata:
        img = np.kron(k, np.ones((12,12)))
        cv2.imwrite(grayfoldername+'/gray%d.jpg' % n, img)
        n = n+1

def SliceFilm(filmlsit, exportfilename, frame_start ,frame_end):
    with open (filmlsit, 'rb') as fp:
        itemlist = pickle.load(fp)
    slice_list = itemlist[frame_start:frame_end]
    with open(exportfilename, 'wb') as fp:
        pickle.dump(slice_list, fp)

def ConvertVideoInFolder(videofolder,datafolder):
    for filename in os.listdir(os.getcwd()+'/'+videofolder):
        CaptureVideoTo6464(videofolder+'/'+filename, datafolder+os.path.splitext(filename)[0])

#Generate image background
def GenCircle(y,x):
    data = np.zeros((64, 64, 4), dtype=np.uint8)
    surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, 64, 64)
    cr = cairo.Context(surface)
    cr.set_source_rgb(0.8, 0.8, 0.8)
    cr.paint()

    r2 = cairo.RadialGradient(x, y, 0, x, y, 10)
    r2.add_color_stop_rgb(0, 0, 0, 0)
    r2.add_color_stop_rgb(0.8, 1, 1, 1)
    cr.set_source(r2)
    cr.arc(x, y, 6, 0, math.pi * 2)
    cr.fill()
    return data[:,:,0]

def GenCirList(exportfilename, x, y, Vx, Vy, fnum):
    circlelist = []
    for i in range(fnum):
        circlelist.append(GenCircle(x+Vx*i,y+Vy*i))
        print i
	
    with open(exportfilename, 'wb') as fp:
        pickle.dump(circlelist, fp)
