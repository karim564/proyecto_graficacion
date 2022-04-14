import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

def estrella(xc,yc,R):
    #angle=np.pi/2
    list_coordiantes = []
    glBegin(GL_LINE_LOOP)
    x=[]
    y=[]
    # x= [
    # xc+R*np.cos(np.pi/2+0*np.pi/5),
    # xc+2/5*R*np.cos(np.pi/2+1*np.pi/5),
    # xc+R*np.cos(np.pi/2+2*np.pi/5),
    # xc+2/5*R*np.cos(np.pi/2+3*np.pi/5),
    # xc+R*np.cos(np.pi/2+4*np.pi/5),
    # xc+2/5*R*np.cos(3*np.pi/2),
    # xc+R*np.cos(np.pi/2+6*np.pi/5),
    # xc+2/5*R*np.cos(np.pi/2+7*np.pi/5),
    # xc+R*np.cos(np.pi/2+8*np.pi/5),
    # xc+2/5*R*np.cos(np.pi/2+9*np.pi/5)];

    for i in range(0,10):
        tempx=0
        tempy=0
        if i%2==0:
            tempx=xc+R*np.cos(np.pi/2+i*np.pi/5)
            tempy=yc+R*np.sin(np.pi/2+i*np.pi/5)
        else:
            tempx=xc+2/5*R*np.cos(np.pi/2+i*np.pi/5)
            tempy=yc+2/5*R*np.sin(np.pi/2+i*np.pi/5)
        x.append(tempx)
        y.append(tempy)
        list_coordiantes.append([tempx,tempy])

    # y= [
    # yc+R*np.sin(np.pi/2),
    # yc+2/5*R*np.sin(np.pi/2+np.pi/5),
    # yc+R*np.sin(np.pi/2+2*np.pi/5),
    # yc+2/5*R*np.sin(np.pi/2+3*np.pi/5),
    # yc+R*np.sin(np.pi/2+4*np.pi/5),
    # yc+2/5*R*np.sin(3*np.pi/2),
    # yc+R*np.sin(np.pi/2+6*np.pi/5),
    # yc+2/5*R*np.sin(np.pi/2+7*np.pi/5),
    # yc+R*np.sin(np.pi/2+8*np.pi/5),
    # yc+2/5*R*np.sin(np.pi/2+9*np.pi/5)];
    #y= [np.sin(np.pi/2),2/5*np.sin(np.pi/2+np.pi/5),np.sin(np.pi/2+2*np.pi/5),2/5*np.sin(np.pi/2+3*np.pi/5),np.sin(np.pi/2+4*np.pi/5),2/5*np.sin(3*np.pi/2),np.sin(np.pi/2+6*np.pi/5),2/5*np.sin(np.pi/2+7*np.pi/5),np.sin(np.pi/2+8*np.pi/5),2/5*np.sin(np.pi/2+9*np.pi/5)];
    glColor3f(1,1,0)
    for i in range(len(x)):
        glVertex2d(x[i],y[i])
    glEnd()
    return list_coordiantes


def spiral(xc,yc,p,n):
    k=1.5
    list_coordiantes=[]
    theta=np.linspace(0,n*math.pi,p);
    glBegin(GL_LINE_STRIP)
    for i in range(p):
        #print(theta[i])
        r=k*theta[i]
        tempx=xc+r*np.cos(theta[i])
        tempy=yc+r*np.sin(theta[i])
        #glColor3f(1,1,1)
        #glVertex2d(tempx,tempy)
        list_coordiantes.append([tempx,tempy])
    glEnd()
    return list_coordiantes

def sol_coordinates(xc,yc,R,n,varg):
    angle=2*np.pi/n
    list_coordiantes = []
    #glColor3f(red,green,blue)
    #glBegin(GL_POLYGON)
    for i in range(n):
        
        x = xc + R*np.cos(angle*i)
        y = yc + R*np.sin(angle*i)
        list_coordiantes.append([x,y])
        glVertex2d(x,y)
        varg+=(1/24)
    #glEnd()
    return list_coordiantes