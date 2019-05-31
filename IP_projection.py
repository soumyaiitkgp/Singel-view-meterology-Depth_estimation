# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:08:40 2019

@author: Predator
"""

import cv2
import math as mt

phi = float(input('Enter the vertical field of view:'))
phi = (phi*mt.pi)/180
P_y = int(input('Enter the number of pixels in vertical direcion:'))
P_x = int(input('Enter the number of pixels in horizontal direcion:'))
h = 0.74 #float(input('Enter the height of the object: '))
#delta = 48.209#float(input('Enter the horizontal angle of the view:'))
#delta = delta*mt.pi/180
delta = mt.atan((P_x/P_y)*mt.tan(phi))
theta = float(input('Enter the tilt angle of the camera: '))
theta = (theta*mt.pi)/180
H = float(input('Enter the height of the camera: '))
cap = cv2.VideoCapture('rtsp://admin:admin123@192.168.0.59:554/Streaming/Channels/701')

#global sbox
global iter

#-----------------------------------------------------------functions----------------------------------------------------------------------

def on_mouse(event, x, y, flags, params):
    global sbox
    if event == cv2.EVENT_LBUTTONDOWN:
        print ('Start Mouse Position: '+str(x)+', '+str(y))
        sbox = [x, y]
        u = sbox[0]
        v = P_y - sbox[1]
        print(u,v)
        
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
            m = [X,Y_1]
        
        else:
            print('Going inside else for m \n')
            Y2 = (-b - mt.sqrt(b*b-4*a*c))/(2*a)
            D2 = (-Y2*mt.tan(theta) + H)/(mt.cos(theta))
            Y_2 = Y2 - D2*mt.sin(theta)
            JK = mt.sqrt(Y2*Y2*(1+mt.tan(theta)*mt.tan(theta)))*(mt.tan(delta))
            X = (((2*u-P_x)*JK)/P_x)
            Y = Y_2
            print('\nThe value of the points are: %d, %d\n',X,Y_2)
            m = [X,Y]
            
        if theta == 0:
            print(m[0],m[1])
            head_Z(m[0], m[1], H, phi, delta, P_y, P_x, h)
            cv2.line(img,(640,0),(640,720),(0,0,255),1)
            cv2.line(img,(sbox[0], sbox[1]),(int(head_z[0]//1),P_y - int(head_z[1]//1)),(255,0,0),1)
            print(int(head_z[0]//1),P_y - int(head_z[1]//1), 'this is jkbkhb')
        else:
            print(m[0],m[1])
            head_NZ(m[0],m[1],H,theta,phi,delta,P_y,P_x, h)
            cv2.line(img,(640,0),(640,720),(0,0,255),1)
            cv2.line(img,(0,360),(1280,360),(0,0,255),1)
            cv2.line(img,(sbox[0], sbox[1]),(int(head_nz[0]//1),P_y - int(head_nz[1]//1)),(255,0,0),1)
            print(int(head_nz[0]//1),P_y - int(head_nz[1]//1), 'this is nz')
        cv2.imshow('real image', img)
        cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            
def head_NZ(X, Y, H, theta, phi, delta, P_y, P_x, h):   #treat head as a base point of the projection of the head on the plane
    global head_nz
    l = (H/(H-h))
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
    u_head = (P_x/2) + ((X*P_x)/(2*Y*mt.tan(delta)));
    v_head = ((P_y*(mt.sqrt((Y*mt.tan(phi)-H)**2))/(2*Y*mt.tan(phi))));
    head_z = [u_head, v_head]

      
#----------------------------------------------------------------------------------------execution------------------------------------------      
iter = 0

while(1):
    # print count
    if iter == 8:
        break
    iter += 1

    phi = float(input('Enter the vertical field of view: '))
    phi = (phi*mt.pi)/180
    delta = mt.atan((P_x/P_y)*mt.tan(phi))
    theta = float(input('Enter the tilt angle of the camera: '))
    theta = (theta*mt.pi)/180
    H = float(input('Enter the height of the camera: '))
    
    while(1):
        ret, img = cap.read()
        
        cv2.line(img,(640,0),(640,720),(0,0,255),1)
        cv2.line(img,(0,360),(1280,360),(0,0,255),1)
        cv2.imshow('frame',img)
        #img = cv2.imread('img_.png',0)
    # img = cv2.blur(img, (3,3))
        img = cv2.resize(img,(1280,720))
        cv2.namedWindow('real image')
        #print(1)
        cv2.setMouseCallback('real image', on_mouse, 0)
        #print(2)
        cv2.imshow('For break press q', img)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    
    '''while(1):
        img  = cv2.imread('img_.png',0)
        #cv2.imshow('frame',img)
        img = cv2.resize(img,(960,720))
        cv2.namedWindow('real image')
        print(1)
        cv2.setMouseCallback('real image', on_mouse, 0)
        cv2.imshow('real image', img)
        print(2)
        if m[0] != 0:
            if theta == 0:
                head_Z(m[0], m[1], H, phi, delta, P_y, P_x)
                cv2.line(img,(sbox[0], sbox[1]),(int(head_z[0]//1),P_y - int(head_z[1]//1)),(255,0,0),5)
                print(int(head_z[0]//1),P_y - int(head_z[1]//1), 'this is jkbkhb')
            else:
                head_NZ(m[0],m[1],H,h,phi,delta,P_y,P_x)
                cv2.line(img,(sbox[0], sbox[1]),(int(head_nz[0]//1),P_y - int(head_nz[1]//1)),(255,0,0),5)
                print(int(head_nz[0]//1),P_y - int(head_nz[1]//1), 'this is nz')
        cv2.imshow('real image', img)
        cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            cv2.destroyAllWindows()'''