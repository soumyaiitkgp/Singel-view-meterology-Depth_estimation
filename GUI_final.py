# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:47:22 2019
@author: Predator
This is the final script of height estimation along with GUI 
"""

import cv2
import math as mt 

P_y = 720
P_x = 1280
cap = cv2.VideoCapture('vehicle1.mp4') #'rtsp://admin:admin123@192.168.0.59:554/Streaming/Channels/101')
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
global iter
boxes = []

#==============================================================================
#function
#==============================================================================

def nothing(x):
    pass

def on_mouse(event, x, y, flags, params):
    global sbox
    if event == cv2.EVENT_LBUTTONDOWN:
        print ('\nStart Mouse Position(OpenCV): '+str(x)+', '+str(y))
        sbox = [x, y]
        u = sbox[0]
        v = P_y - sbox[1]
        print('Foot point(Model):',u,v)
        
        if v <= P_y/2:   
            l = (1-(2*v/P_y))
        else:
            l = ((2*v/P_y)-1)
        
        a = (mt.tan(theta)*mt.tan(theta) - l*l*mt.tan(phi)*mt.tan(phi)*mt.cos(theta)*mt.cos(theta) - l*l*mt.tan(phi)*mt.tan(phi)*mt.cos(theta)*mt.cos(theta)*mt.tan(theta)*mt.tan(theta))
        b = (-2*H*mt.tan(theta))
        c = (H*H)
        
        if v >= P_y/2:
            Y1 = (-b + mt.sqrt(b*b-4*a*c))/(2*a)
            D1 = (-Y1*mt.tan(theta) + H)/(mt.cos(theta))
            Y_1 = Y1 - D1*mt.sin(theta)
            JK = mt.sqrt(Y1*Y1*(1+mt.tan(theta)*mt.tan(theta)))*(mt.tan(delta))
            X = (2*u-(P_x))*((JK)/P_x)
            print('\nThe world coordinates of the starting points are:','(',X,Y_1,')','m')
            m = [X,Y_1]
            
        else:
            Y2 = (-b - mt.sqrt(b*b-4*a*c))/(2*a)
            D2 = (-Y2*mt.tan(theta) + H)/(mt.cos(theta))
            Y_2 = Y2 - D2*mt.sin(theta)
            JK = mt.sqrt(Y2*Y2*(1+mt.tan(theta)*mt.tan(theta)))*(mt.tan(delta))
            X = (((2*u-P_x)*JK)/P_x)
            Y = Y_2
            print('\nThe world coordinates of the points are:','(',X,Y_2,')','m')
            m = [X,Y]
            
        if theta == 0:
            head_Z(m[0], m[1], H, phi, delta, P_y, P_x, h)
            cv2.line(img,(sbox[0], sbox[1]),(int(head_z[0]//1),P_y - int(head_z[1]//1)),(0,0,0),3)
            print('The height of the object is:', h)
            print('\nThe coordinates of the head points are(OpenCV):',int(head_z[0]//1),P_y - int(head_z[1]//1))
            print('Head point(Model): ',int(head_z[0]//1),int(head_z[1]//1),head_z[1])
            print('==========================================================')

        else:
            head_NZ(m[0],m[1],H,theta,phi,delta,P_y,P_x, h)
            cv2.line(img,(sbox[0], sbox[1]),(int(head_nz[0]//1),P_y - int(head_nz[1]//1)),(0,255,0),3)
            print('The height of the object is:', h)
            print('\nThe coordinates of the head points are(OpenCV):',int(head_nz[0]//1),P_y - int(head_nz[1]//1))
            print('Head point(Model): ',int(head_nz[0]//1),int(head_nz[1]//1))
            print('==========================================================')
        cv2.imshow('real image', img)
        cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

def head_NZ(X, Y, H, theta, phi, delta, P_y, P_x, h):   #treat head as a base point of the projection of the head on the plane
    global head_nz
    l = (H/(H-h))
    if l < 0:
        l = -l
    Y = l*Y
    X = l*X
    x = ((H+Y*(1/mt.tan(theta)))/(mt.tan(theta+phi)+(1/mt.tan(theta))))
    y = ((-(H+Y*(1/mt.tan(theta))*(mt.tan(theta+phi))))/(mt.tan(theta+phi)+(1/mt.tan(theta))))+H
    a = (y-H)
    d = (x*x + (a)**2)**0.5
    MP = 2*d*mt.sin(phi)
    MX = ((x-Y)**2 + y*y)**0.5
    v_head = (MX/MP)*P_y
    JK = d*mt.cos(phi)*mt.tan(delta)
    u_head = (P_x/2) +(X/(2*JK))*P_x
    head_nz = [u_head,v_head]
    return head_nz

def head_Z(X,Y,H,phi,delta,P_y,P_x, h):
    global head_z
    
    l = (H/(H-h))
    Y = l*Y
    X = l*X
    if l < 0:
        l = -l    
    #v_head = ((P_y*(mt.sqrt((Y*mt.tan(phi)-H)**2))/(2*Y*mt.tan(phi)))) old
    u_head = (P_x/2) + ((X*P_x)/(2*Y*mt.tan(delta)))
    v_head = P_y*((Y*mt.tan(phi)+(H-h))/(2*Y*mt.tan(phi)))
    head_z = [u_head, v_head]

#==============================================================================
#function2
#==============================================================================

def on_mouse1(event, x, y, flags, params):          #function for measuring height/depth by cursor
    
    global iter
    global sbox
    global ebox
    global bbox
    global hbox
    
    if event == cv2.EVENT_LBUTTONDOWN:
        ebox = [0,0]
        print('Start Mouse Position: '+str(x)+', '+str(y))
        sbox = [x, y]
        boxes.append(sbox)
        u = sbox[0]
        v = P_y - sbox[1]
        print('Image coordinates:',u,v)
            
        if v <= P_y/2:   
            l = (1-(2*v/P_y))
        else:
            l = ((2*v/P_y)-1)
        
        a = (mt.tan(theta)*mt.tan(theta) - l*l*mt.tan(phi)*mt.tan(phi)*mt.cos(theta)*mt.cos(theta) - l*l*mt.tan(phi)*mt.tan(phi)*mt.cos(theta)*mt.cos(theta)*mt.tan(theta)*mt.tan(theta))
        b = (-2*H*mt.tan(theta))
        c = (H*H)
        
        if v >= P_y/2:
            Y1 = (-b + mt.sqrt(b*b-4*a*c))/(2*a)
            D1 = (-Y1*mt.tan(theta) + H)/(mt.cos(theta))
            Y_1 = Y1 - D1*mt.sin(theta)
            JK = mt.sqrt(Y1*Y1*(1+mt.tan(theta)*mt.tan(theta)))*(mt.tan(delta))
            X = (2*u-(P_x))*((JK)/P_x)
            print('\nThe value of the points are: (%d, %d\n)',X,Y_1)
            bbox = [X,Y_1]
        
        else:
            print('Going inside else for m \n')
            Y2 = (-b - mt.sqrt(b*b-4*a*c))/(2*a)
            D2 = (-Y2*mt.tan(theta) + H)/(mt.cos(theta))
            Y_2 = Y2 - D2*mt.sin(theta)
            JK = mt.sqrt(Y2*Y2*(1+mt.tan(theta)*mt.tan(theta)))*(mt.tan(delta))
            X = (((2*u-P_x)*JK)/P_x)
            Y = Y_2
            print('\nThe value of the points are: %d, %d\n',X,Y_2)
            bbox = [X,Y] 

    elif event == cv2.EVENT_LBUTTONUP:
        print('End Mouse Position: '+str(x)+', '+str(y))
        ebox = [x, y]
        boxes.append(ebox)
        print(boxes)
        U = ebox[0]
        V = P_y - ebox[1]
        
        if V <= P_y/2:   
            l = (1-(2*V/P_y))
        else:
            l = ((2*V/P_y)-1)
        
        a = (mt.tan(theta)*mt.tan(theta) - l*l*mt.tan(phi)*mt.tan(phi)*mt.cos(theta)*mt.cos(theta) - l*l*mt.tan(phi)*mt.tan(phi)*mt.cos(theta)*mt.cos(theta)*mt.tan(theta)*mt.tan(theta))
        b = (-2*H*mt.tan(theta))
        c = (H*H)
        
        if V >= P_y/2:
            Y1 = (-b + mt.sqrt(b*b-4*a*c))/(2*a)
            D1 = (-Y1*mt.tan(theta) + H)/(mt.cos(theta))
            Y_1 = Y1 - D1*mt.sin(theta)
            JK = mt.sqrt(Y1*Y1*(1+mt.tan(theta)*mt.tan(theta)))*(mt.tan(delta))
            X = (2*U-(P_x))*((JK)/P_x)
            print('\nThe value of the points are(for head): (%d, %d\n)',X,Y_1)
            hbox = [X,Y_1]
        
        else:
            print('Going inside else for m \n')
            Y2 = (-b - mt.sqrt(b*b-4*a*c))/(2*a)
            D2 = (-Y2*mt.tan(theta) + H)/(mt.cos(theta))
            Y_2 = Y2 - D2*mt.sin(theta)
            JK = mt.sqrt(Y2*Y2*(1+mt.tan(theta)*mt.tan(theta)))*(mt.tan(delta))
            X = (((2*U-P_x)*JK)/P_x)
            Y = Y_2
            print('\nThe value of the points are(for head): ',X,Y_2)
            hbox = [X,Y] 
            iter = 1
        
        h = H*(hbox[1]-bbox[1])/(hbox[1])
        print("The height of the object is:", h)
        cv2.line(img,(int(sbox[0]),int(sbox[1])),(int(ebox[0]),int(ebox[1])),(255,0,0),1)
        cv2.imshow('real image', img)
        h = str(h)
        hbox = str(hbox)
        app = QApplication([])
        win = QMainWindow()
        button = QPushButton('Height of the object: ' + h+ ' m' + '\nWorld coordinates of the object: ' + hbox + ' m')
        win.setCentralWidget(button)
        win.show()
        app.exit(app.exec_())
        
#==============================================================================
        #function3
#==============================================================================
        
def base_NZ(X, Y, H, theta, phi, delta, P_y, P_x):   #function for projection of lines on the virtual plane or grids
    global base_nz
    x = ((H+Y*(1/mt.tan(theta)))/(mt.tan(theta+phi)+(1/mt.tan(theta))))
    y = ((-(H+Y*(1/mt.tan(theta))*(mt.tan(theta+phi))))/(mt.tan(theta+phi)+(1/mt.tan(theta))))+H
    a = (y-H)
    d = (x*x + (a)**2)**0.5
    MP = 2*d*mt.sin(phi)
    MX = ((x-Y)**2 + y*y)**0.5
    v_base = P_y - (MX/MP)*P_y
    JK = d*mt.cos(phi)*mt.tan(delta)
    u_base = (P_x/2) +(X/(2*JK))*P_x
    base_nz = [u_base,v_base]
    return base_nz

def base_Z(X,Y,H,phi,delta,P_y,P_x):
    global base_z
    u_base = (P_x/2) + ((X*P_x)/(2*Y*mt.tan(delta)))
    v_base = P_y - ((P_y*(mt.sqrt((Y*mt.tan(phi)-H)**2))/(2*Y*mt.tan(phi))))
    base_z = [u_base, v_base]
    return base_z

#==============================================================================
#commmand
#==============================================================================

while(1):
    ret, img = cap.read()
    #img = cv2.imread('tt3.jpg')
    img = cv2.resize(img,(int(P_x),int(P_y)))
    cv2.imshow('To capture press q',img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("test.png", img)
        cv2.destroyAllWindows()
        break
       
iter = 0
cv2.namedWindow('image')
cv2.resizeWindow('image', 1576,144) 
cv2.createTrackbar('Height(cm)','image',1,5000,nothing) #edit 5000 for sdjusting height limit
cv2.createTrackbar('theta','image',0,900,nothing) 
cv2.createTrackbar('phi','image',1,900,nothing)
cv2.createTrackbar('h(cm)','image',1,4000,nothing)
cv2.createTrackbar('Confirm','image',0,1,nothing)
cv2.createTrackbar('Measure distance','image',0,1,nothing)
cv2.createTrackbar('Grid','image',0,1,nothing)
cv2.createTrackbar('Grid density','image',0,50,nothing)
cv2.setTrackbarPos('Height(cm)', 'image', 100)
cv2.setTrackbarPos('theta', 'image', 50)
cv2.setTrackbarPos('phi', 'image', 200)
cv2.setTrackbarPos('h(cm)', 'image', 200)
cv2.setTrackbarPos('Grid density', 'image', 5)

H = 1
theta = 0.1
phi = 0.1
h = 1

while(1):
    # print count
    if iter == 1:
        break
    iter += 1

    while(1):
        
        H = cv2.getTrackbarPos('Height(cm)','image')
        H = H/100
        theta = cv2.getTrackbarPos('theta','image')
        theta = (theta*mt.pi)/1800
        phi = cv2.getTrackbarPos('phi','image')
        if phi == 0:
            phi = 1
            cv2.setTrackbarPos('phi', 'image', 1)
        phi = (phi*mt.pi)/1800
        h = cv2.getTrackbarPos('h(cm)','image')
        h = h/100
        s = cv2.getTrackbarPos('Confirm','image')
        gd = cv2.getTrackbarPos('Grid density','image')
        if gd == 0:
            gd = 1
            cv2.setTrackbarPos('Grid density', 'image', 1)
        delta = mt.atan((P_x/P_y)*mt.tan(phi))
        #img = cv2.imread('img_.png',0) # for image read
        img = cv2.imread('test.png')
        img = cv2.resize(img,(int(P_x),int(P_y)))
        
#-----------------------------------for grid making----------------------------
        g = cv2.getTrackbarPos('Grid','image')
        if g == 1:
            for X in range(-50,51,gd): #adjust this value for densing or sparsing of grids, default distance is 5 m
                for Y in range(25,250,gd): 
                    if theta == 0: # for lines along x-axis
                        #print('This is delta:',delta)
                        p = base_Z(-50,Y,H,phi,delta,P_y,P_x)
                        q = base_Z(50,Y,H,phi,delta,P_y,P_x)
                        cv2.line(img,(int(p[0]),int(p[1])),(int(q[0]),int(q[1])),(0,0,255),1)
                    if theta != 0: #for lines along x-axis
                        p = base_NZ(-50,Y,H,theta,phi,delta,P_y,P_x)
                        q = base_NZ(50,Y,H,theta,phi,delta,P_y,P_x)
                        cv2.line(img,(int(p[0]),int(p[1])),(int(q[0]),int(q[1])),(0,0,255),1)
                

                    if theta == 0: # for lines along y-axis
                        p = base_Z(X,1,H,phi,delta,P_y,P_x)
                        #print('The value of starting point:', X, p[0], P_y -p[1])
                        q = base_Z(X,500,H,phi,delta,P_y,P_x)
                        #print('The value of ending point:',X, q[0], P_y -q[1])
                        cv2.line(img,(int(p[0]),P_y - int(p[1])),(int(q[0]),int(q[1])),(255,0,0),1)
                    if theta != 0: #for lines along x-axis
                        p = base_NZ(X,1,H,theta,phi,delta,P_y,P_x)
                        #print('The value of starting point:',X, p[0], P_y -p[1])                    
                        q = base_NZ(X,500,H,theta,phi,delta,P_y,P_x)
                        cv2.line(img,(int(p[0]),P_y - int(p[1])),(int(q[0]), int(q[1])),(255,0,0),1)
            
            for X in range(-50,51,gd):
                for Y in range(250,500,3*gd):
                    if theta == 0: # for lines along x-axis
                        #print('This is delta:',delta)
                        p = base_Z(-50,Y,H,phi,delta,P_y,P_x)
                        q = base_Z(50,Y,H,phi,delta,P_y,P_x)
                        cv2.line(img,(int(p[0]),int(p[1])),(int(q[0]),int(q[1])),(0,0,255),1)
                    if theta != 0: #for lines along x-axis
                        p = base_NZ(-50,Y,H,theta,phi,delta,P_y,P_x)
                        q = base_NZ(50,Y,H,theta,phi,delta,P_y,P_x)
                        cv2.line(img,(int(p[0]),int(p[1])),(int(q[0]),int(q[1])),(0,0,255),1)
                

                    if theta == 0: # for lines along y-axis
                        p = base_Z(X,1,H,phi,delta,P_y,P_x)
                        #print('The value of starting point:', X, p[0], P_y -p[1])
                        q = base_Z(X,500,H,phi,delta,P_y,P_x)
                        #print('The value of ending point:',X, q[0], P_y -q[1])
                        cv2.line(img,(int(p[0]),P_y - int(p[1])),(int(q[0]),int(q[1])),(0,255,0),1)
                    if theta != 0: #for lines along x-axis
                        p = base_NZ(X,1,H,theta,phi,delta,P_y,P_x)
                        #print('The value of starting point:',X, p[0], P_y -p[1])                    
                        q = base_NZ(X,500,H,theta,phi,delta,P_y,P_x)
                        cv2.line(img,(int(p[0]),P_y - int(p[1])),(int(q[0]), int(q[1])),(0,255,0),1)

                            
        #----------------------------------end--------------------------------- 
        
        cv2.namedWindow('real image')
        cv2.setMouseCallback('real image', on_mouse, 0)
        cv2.imshow('real image',img)
        cv2.waitKey(1)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        if s == 1:
            break
        
#==============================================================================
#command2
#==============================================================================
            
m = cv2.getTrackbarPos('Measure distance','image')
if  s == 1:
    if m ==1:    
        sbox = [0,0]
        ebox = [0,0]    
        count = 0
        
        while(1):
            if iter == 2:
                break
            img = cv2.imread('test.png',0) # for image read
            img = cv2.resize(img,(int(P_x),int(P_y)))
            cv2.namedWindow('real image')
            cv2.setMouseCallback('real image', on_mouse1, 0)
            
            if count < 50:
                if cv2.waitKey(33) == 27:
                    cv2.destroyAllWindows()
                    break
            elif count >= 50:
                count = 0
                
#==============================================================================
                #end
#==============================================================================