import numpy as np
import cv2 as cv

#The function
def hough(edge_img,thresh):

    pnts=[] 
    indices = np.where(edge_img!=0)    #collecting the co-ordinates of edge pixels
    pnts = zip(indices[0], indices[1])  

    w,h = edge_img.shape
    d_max = np.ceil(np.sqrt((w*w)+(h*h)))    #getting the maximum value that rho can have
    d_max = int(d_max)
    
    H=np.zeros(shape=(2*d_max,180))     #initializing the accumulator array

    for point in pnts:
        for a in range(-90,90):
            d = (point[0]*np.cos(np.deg2rad(a)) - (point[1]*np.sin(np.deg2rad(a))))
            H[int(d)+d_max,a+90]+=1   #calculating d, and incrementing the values in the accumulator array

    lines = []
    points = np.where(H>thresh)     #getting the location of points where value is greater than the threshold

    points = np.array(points)
    points[0] = points[0] - d_max

    lines = zip(points[0], points[1])   #appending those locations in the array to be returned

    return lines                           
              

img = cv.imread(r'D:\UserData\Documents\Projects\Hough Lines\sudoku.png')     
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray,50,150,apertureSize = 3)  #getting edges

lines = hough(edges, 195)    #calling the funtions

for line in lines:      #getting values of rho and theta, to draw identify and draw lines
    (rho,theta) = line

    a = np.cos(np.deg2rad(theta))
    b = np.sin(np.deg2rad(theta))

    x0 = a*rho
    y0 = b*rho

    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv.imshow('houghlines3.jpg',img)
