import numpy as np
import cv2 

def connectedComponent(img):

    global parent_label
    parent_label=[]
    count = 1
    non_zero = []

    h,w = img.shape

    #FIRST PASS#
    for i in range(2,img.shape[0]-1):
        for j in range(2,img.shape[1]-1):
            if img[i,j]==255:

                ngbrs = np.array([img[i-1,j-1], img[i,j-1], img[i-1,j], img[i-1,j+1], img[i-2,j+1], img[i-2,j], img[i-2,j-1]]) #declaring the neighbouring points
            
                if np.count_nonzero(ngbrs==0)==7 : #if a new space, assign new no.
                    img[i,j] = count
                    count+=1
                    
                elif np.count_nonzero(ngbrs) == 1: #if only 1 neighbour has a label
                    b = np.nonzero(ngbrs)
                    img[i,j] = ngbrs[b]

                else:     #if more than 1 neighbours labels
                    a = min(min(ngbrs[i] for i in np.nonzero(ngbrs)))   #assign the current element with the min neighbouring label
                    img[i,j] = a    

                    indices = np.nonzero(ngbrs)    #getting indexes of non-zero elements
                    for k in indices[0]:        
                        if a!=ngbrs[k]:     #ngbrs[k], has all the labels other than the min label
                            parent_label.append([ngbrs[k],a])   #creating the equivivalence matrix, 1st col has the values that should be changing to 2nd col values 

    parent_label = np.transpose(parent_label) #makes our work easier, as then we'll have only 2 rows
    
    try:
        l = len(parent_label[0])

        while len(set(parent_label[0])&set(parent_label[1]))!=0:    #Checking the intersection. Till all the values of 2nd row aren't changed, it'll keep running   
            for index,i in enumerate(parent_label[0]) :             #For e.g, if there 9->8, 10->9 and 11->10, what we want is 9->8, 10->8 and 11->8

                if np.count_nonzero(parent_label[1]==i)!=0:
                    ind = np.nonzero(parent_label[1]==i)
                    parent_label[1,ind]=parent_label[1,index] #changing the value of second row
                
    #SECOND PASS#
        for i in range(img.shape[0]):               #changing the labels using equivalency matrix i.e. parent_label
            for j in range(img.shape[1]):

                if img[i,j]!=0:
                    if img[i,j] in parent_label[0]:
                        ind = np.where(parent_label[0]==img[i,j])
                        img[i,j] = parent_label[1, min(ind[0])]

    except IndexError as i:
       pass 
                         
    return(img)


def imshow_components(labels): #function for displaying in different colours

    label_hue = np.uint8(100*labels)  #creating the channel hue, using labelled image
    blank_ch = 255*np.ones_like(label_hue) #creating 2 blank channels, for saturation and value
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch]) #creating the HSV image, by mearging the 3 channels

    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR) 

    labeled_img[label_hue==0] = 0  #turning backgrougd pixels black

    cv2.imshow('labeled.png', labeled_img) 

image = cv2.imread(r'C:\Users\HP\Pictures\Technoseason\eGaIy.jpg',0)
_,image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)   #to ensure it's binary

cv2.imshow('',image)
label_img = connectedComponent(image)
imshow_components(label_img)
