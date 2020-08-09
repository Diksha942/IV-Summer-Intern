import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def nothing(x):
    pass

#function to draw a rectangle wherw the stylus has to be placed
def draw_rect(frame):
    global x,y
    row,col,_=frame.shape
    y=np.uint32((col/2)-12)
    x=np.uint32((row/2)-12)
    cv.rectangle(frame,(y,x),(y+24,x+24),(0,255,0),1)
    return(frame)

#Window where it'll draw 
cv.namedWindow('Drawing Board')

cv.createTrackbar("R", "Drawing Board", 0, 255, nothing)
cv.createTrackbar("G", "Drawing Board", 0, 255, nothing)
cv.createTrackbar("B", "Drawing Board", 0, 255, nothing)
cv.createTrackbar("Size", "Drawing Board", 3, 30, nothing)

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(30,30))
#kernel2 = np.ones((5,5))
points = []
hist_flag = 0
cont_flag=0

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print('Cannot open camera')
    exit()

while True:
    ret, frame = cap.read()
    if not ret :
        print("Can't recieve frame, try again later maybe...")
        break
    frame = cv.flip(frame,1)
    hsv=cv.cvtColor(frame,cv.COLOR_BGR2HSV)

    #Input the colour range if Enter is pressed
    if cv.waitKey(10)&0xff==13:
        roi=np.zeros([24,24,3], dtype=hsv.dtype)
        roi[0:24,0:24]=hsv[x:x+24,y:y+24]
        hist_flag=1
    else:
        frame=draw_rect(frame)
        cv.imshow('Original',frame)

    #compute histograms of the colour range input
    if hist_flag==1:
        
        hist = cv.calcHist([roi],[0,1],None,[180,256],[0,180,0,256])
        cv.normalize(hist, hist,0,255,cv.NORM_MINMAX)
        dst = cv.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)

        #try clearing the noise
        dst=cv.morphologyEx(dst,cv.MORPH_CLOSE,kernel)
        #dst=cv.dilate(dst, kernel2,iterations=1)

        #making the mask
        ret, thresh = cv.threshold(dst,127, 255, cv.THRESH_BINARY)
        thresh1 = cv.merge((thresh, thresh, thresh))

        masked = cv.bitwise_and(frame,thresh1)
        cnt,_ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        #if contour is detected, move forward
        if len(cnt)>0:

            c = max(cnt, key = cv.contourArea)

            #drawing a rectangle around
            rect = cv.minAreaRect(c)
            global cx,cy
            [(cx,cy),(w,h),_] = rect
            box = cv.boxPoints(rect)
            box = np.int0(box)

            cv.drawContours(masked,[box],0,(0,0,255),2)
            cv.circle(masked,(int(cx),int(cy)),3,(255,0,0),-1)
            cv.imshow('Original', masked)
            
            board = np.zeros(frame.shape, np.uint8)
            board[:] = [255,255,255]
            brd_flag=1

            #trackbars to set colour and size of the pen
            r = cv.getTrackbarPos("R", "Drawing Board")
            g = cv.getTrackbarPos("G", "Drawing Board")
            b = cv.getTrackbarPos("B", "Drawing Board")
            sz = cv.getTrackbarPos("Size", "Drawing Board")

        else:
            continue
        #works as a pointer
        cv.circle(board,(int(cx),int(cy)),sz,(b,g,r),-1)
        #stops drawing when pressed p
        if cv.waitKey(40)&0xff==ord('p'):
            points.append((0,0))
        else:
            points.append((int(cx), int(cy)))
        for i in range(1,len(points)):
            if points[i]==(0,0):
                pass
            else:
                if points[i-1]==(0,0):
                    pass
                else:
                    cv.line(board,points[i-1],points[i],(b,g,r),sz)
                cv.imshow('Drawing Board', board)
            
    if cv.waitKey(1)&0xff == 27:
        break
    #clears the board when pressed c
    if cv.waitKey(5)&0xff == ord('c'):
        points[:]=[]
        continue

cap.release()
cv.destroyAllWindows()
