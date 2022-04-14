from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from modules.textures import loadTexture
from modules.gameobject import GameObject
from modules.bezier import *
from modules.draw import *
from modules.play import *
from threading import Thread
from modules.transforms import *
import numpy as np
import random
import math

w,h= 1000,500

#TEXTURA DE FONDO
texture_background = []

#TEXTURA PLATAFORMA
texture_platform = []
GROUND = 50

#TEXTURA DE SPIDERMAN
SPIDERMAN_IDLE = 0
SPIDERMAN_RUN = 1
SPIDERMAN_JUMP = 2
texture_spiderman = []

#TEXTURA DE VENOM
VENOM_IDLE = 0
VENOM_RUN = 1
VENOM_JUMP = 2
texture_venom = []

#TEXTURA GREEN GLOBIN
texture_green_globin = []

#Movimiento Spiderman
flag_left_spiderman = False
flag_right_spiderman = False
flag_up_spiderman = False

#Movimiento Venom
flag_left_venom = False
flag_right_venom = False
flag_up_venom = False

#Elementos de Spiderman
spiderman_gameobject = GameObject()

green_gameobject = GameObject()
venom_gameobject = GameObject()

def draw_poste():
    glColor3f(0,0.08,0.3)
    glBegin(GL_POLYGON)
    glVertex2d(480,200)
    glVertex2d(480,300)
    glVertex2d(490,300)
    glVertex2d(490,200)
    glEnd()
    glLineWidth(3)
    a=spiral(485,300,np.random.randint(5,100),np.random.randint(2,16))
    #points = np.array([[200,200],[300,300],[400,200],[100,400]])
    points = np.array(a)
    paths=evaluate_bezier(points,1)
    path_x,path_y=paths[:,0],paths[:,1]
    glColor3f(0.8,0.8,0.8)
    glBegin(GL_LINE_STRIP)
    for i in range(len(path_x)-1):
        glColor3f(0.6,0.16,0.4)
        glVertex2d(path_x[i],path_y[i])
    glEnd()


def draw_sol():
    varg = 0.25
    sol_coord = sol_coordinates(800,400,50,32,varg)
    sol_coord = translate(sol_coord,-850,-400)
    sol_coord = resize(sol_coord,0.8,0.8)
    sol_coord = rotate(sol_coord, 3.141592)
    sol_coord = translate(sol_coord, 850,400)
    glBegin(GL_POLYGON)
    for i in range(len(sol_coord)):
        glColor3f(1,varg,0)
        glVertex2d(sol_coord[i][0], sol_coord[i][1])
        varg+=(1/24)
    glEnd()

def draw_estrellas():
    xc1=112
    yc1=320
    xc2=500
    yc2=460
    xc3=850
    yc3=250
    cord_estrella=[
        estrella(xc1,yc1,16),
        estrella(xc2,yc2,24),
        estrella(xc3,yc3,32)]
    cord_estrella=[
    translate(cord_estrella[0],-xc1,-yc1),
    translate(cord_estrella[1],-xc2,-yc2),
    translate(cord_estrella[2],-xc3,-yc3)]
    randomsillo=np.random.random()
    
    newestrella=[
        resize(cord_estrella[0],randomsillo*5,randomsillo*5),
        rotate(cord_estrella[1],randomsillo*2*math.pi),
        translate(cord_estrella[2],randomsillo*-400,0)
        ]
    #newestrella=rotate(newestrella,3.1416)

    newestrella=[
        translate(newestrella[0],xc1+50,yc1+50),
        translate(newestrella[1],xc2+100,yc2),
        translate(newestrella[2],xc3,yc3)]
    #glLineWidth(2)

    for j in range(len(newestrella)):
        glBegin(GL_LINE_LOOP)
        for i in range(len(newestrella[0])):
            glColor3f(0,0.5,1)

            glVertex2d(newestrella[j][i][0], newestrella[j][i][1])
        #glVertex2d(newestrella[1][i][0], newestrella[1][i][1])
        glEnd() 

def draw_background():
    global texture_background, texture_platform
    glBindTexture(GL_TEXTURE_2D, texture_background)
    glBegin(GL_POLYGON)
    glTexCoord2f(0,0)
    glVertex2d(0,0)
    glTexCoord2f(1,0)
    glVertex2d(w,0)
    glTexCoord2f(1,1)
    glVertex2d(w,h)
    glTexCoord2f(0,1)
    glVertex2d(0,h)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, texture_platform)
    glBegin(GL_POLYGON)
    glTexCoord2f(0,0)
    glVertex2d(0,0)
    glTexCoord2f(1,0)
    glVertex2d(w,0)
    glTexCoord2f(1,1)
    glVertex2d(w,200)
    glTexCoord2f(0,1)
    glVertex2d(0,200)
    glEnd()

   
#Dibujar Green Globin
def draw_green_globin():
    global green_gameobject
    x,y = green_gameobject.get_position()
    w,h = green_gameobject.get_size()
    pin_x_start, pin_x_end = (1,0) if green_gameobject.is_mirrored() else (0,1)
    glBindTexture(GL_TEXTURE_2D, green_gameobject.get_frame_to_draw())
    glBegin(GL_POLYGON)
    glTexCoord2f(pin_x_start,0)
    glVertex2d(x,y)
    glTexCoord2f(pin_x_end,0)
    glVertex2d(x+w,y)
    glTexCoord2f(pin_x_end,1)
    glVertex2d(x+w,y+h)
    glTexCoord2f(pin_x_start,1)
    glVertex2d(x,y+h)
    glEnd()


#Dibujar Spiderman
def draw_spiderman():
    global spiderman_gameobject
    x,y = spiderman_gameobject.get_position()
    w,h = spiderman_gameobject.get_size()
    pin_x_start, pin_x_end = (1,0) if spiderman_gameobject.is_mirrored() else (0,1)
    glBindTexture(GL_TEXTURE_2D, spiderman_gameobject.get_frame_to_draw())
    glBegin(GL_POLYGON)
    glTexCoord2f(pin_x_start,0)
    glVertex2d(x,y)
    glTexCoord2f(pin_x_end,0)
    glVertex2d(x+w,y)
    glTexCoord2f(pin_x_end,1)
    glVertex2d(x+w,y+h)
    glTexCoord2f(pin_x_start,1)
    glVertex2d(x,y+h)
    glEnd()

#Dibujar Venom
def draw_venom():
    global venom_gameobject
    x,y = venom_gameobject.get_position()
    w,h = venom_gameobject.get_size()
    pin_x_start, pin_x_end = (1,0) if venom_gameobject.is_mirrored() else (0,1)

    glBindTexture(GL_TEXTURE_2D, venom_gameobject.get_frame_to_draw())
    glBegin(GL_POLYGON)
    glTexCoord2f(pin_x_start,0)
    glVertex2d(x,y)
    glTexCoord2f(pin_x_end,0)
    glVertex2d(x+w,y)
    glTexCoord2f(pin_x_end,1)
    glVertex2d(x+w,y+h)
    glTexCoord2f(pin_x_start,1)
    glVertex2d(x,y+h)
    glEnd()


def check_collisions():
    global spiderman_gameobject, venom_gameobject
    if spiderman_gameobject.is_collision(venom_gameobject):
        spiderman_gameobject = GameObject(random.randint(0,w),GROUND,(int)(226/4),(int)(282/4), texture_spiderman)
        thread_sound_venom = Thread(target=play_venom)
        thread_sound_venom.start()



def keyPressed ( key, x, y):
    global flag_left_spiderman, flag_right_spiderman, flag_up_spiderman, flag_down_spiderman
    global flag_left_venom, flag_right_venom, flag_up_venom, flag_down_venom
    if key == b'\x1b':
        glutLeaveMainLoop()
    if key == b'w':
        flag_up_spiderman = True
        
    if key == b's':
        flag_down_spiderman = True
        
    if key == b'a':
        flag_left_spiderman = True
        
    if key == b'd':
        flag_right_spiderman = True

    if key == b'u':
        flag_up_venom = True
    
    if key == b'j':
        flag_down_venom = True
    
    if key == b'h':
        flag_left_venom = True
    
    if key == b'k':
        flag_right_venom = True
        
def keyUp(key, x, y):
    global flag_left_spiderman, flag_right_spiderman, flag_up_spiderman, flag_down_spiderman
    global flag_left_venom, flag_right_venom, flag_up_venom, flag_down_venom
    if key == b'w':
        flag_up_spiderman = False
    if key == b's':
        flag_down_spiderman = False
    if key == b'a':
        flag_left_spiderman = False
    if key == b'd':
        flag_right_spiderman = False
    if key == b'u':
        flag_up_venom = False
    if key == b'j':
        flag_down_venom = False
    if key == b'h':
        flag_left_venom = False
    if key == b'k':
        flag_right_venom = False
        

def init():
    glClearColor ( 0.0, 0.0, 0.0, 0.0 )
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    

def reshape(width, height):
    global w, h
    glViewport ( 0, 0, width, height )
    glMatrixMode ( GL_PROJECTION )
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    w = width
    h = height
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

def display():
    glClear ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

    #---------------------DIBUJAR AQUI------------------------#
    draw_background()
    draw_sol()
    draw_poste()
    draw_estrellas()
    glColor3f(1,1,1)
    draw_spiderman()
    draw_venom()
    draw_green_globin()
    #---------------------------------------------------------#

    glutSwapBuffers()

def animate():
    temp = 0

#TIMERS
def timer_move_spiderman(value):
    global spiderman_gameobject, flag_left_spiderman, flag_right_spiderman, flag_up_spiderman
    global SPIDERMAN_IDLE, SPIDERMAN_RUN, SPIDERMAN_DOWN, SPIDERMAN_JUMP
    state = spiderman_gameobject.get_state()
    input = {'x': 0, 'y': 0}
    input['y'] = 1 if flag_up_spiderman else 0
    if flag_right_spiderman:
        input['x'] = 1
    elif flag_left_spiderman:
        input['x'] = -1


    if flag_up_spiderman:
        if state != SPIDERMAN_JUMP:
            spiderman_gameobject.change_state(SPIDERMAN_JUMP)
            thread_jump = Thread(target=play_jump)
            thread_joke = Thread(target=play_joke)
            thread_joke.start()
            thread_jump.start()
    elif flag_right_spiderman:
        if state != SPIDERMAN_RUN:
            spiderman_gameobject.change_state(SPIDERMAN_RUN)
        if spiderman_gameobject.is_mirrored():
            spiderman_gameobject.set_mirror(False)
    elif flag_left_spiderman:
        if state != SPIDERMAN_RUN:
            spiderman_gameobject.change_state(SPIDERMAN_RUN)
        if not spiderman_gameobject.is_mirrored():
            spiderman_gameobject.set_mirror(True)
    else:
        if state != SPIDERMAN_IDLE:
            spiderman_gameobject.change_state(SPIDERMAN_IDLE)
    

    check_collisions()
    spiderman_gameobject.move(input)
    glutPostRedisplay()
    glutTimerFunc(20, timer_move_spiderman, 1)

def timer_animate_spiderman(value):
    global spiderman_gameobject
    spiderman_gameobject.animate()
    glutPostRedisplay()
    glutTimerFunc(100, timer_animate_spiderman, 1)


def timer_move_venom(value):
    global venom_gameobject, flag_left_venom, flag_right_venom, flag_up_venom
    global VENOM_IDLE, VENOM_RUN, VENOM_DOWN, VENOM_JUMP
    state = venom_gameobject.get_state()
    input = {'x': 0, 'y': 0}
    input['y'] = 1 if flag_up_venom else 0
    if flag_right_venom:
        input['x'] = 1
    elif flag_left_venom:
        input['x'] = -1


    if flag_up_venom:
        if state != VENOM_JUMP:
            venom_gameobject.change_state(VENOM_JUMP)
            thread_jump = Thread(target=play_jump)
            thread_jump.start()
    elif flag_right_venom:
        if state != VENOM_RUN:
            venom_gameobject.change_state(VENOM_RUN)
        if venom_gameobject.is_mirrored():
            venom_gameobject.set_mirror(False)
    elif flag_left_venom:
        if state != VENOM_RUN:
            venom_gameobject.change_state(VENOM_RUN)
        if not venom_gameobject.is_mirrored():
            venom_gameobject.set_mirror(True)
    else:
        if state != VENOM_IDLE:
            venom_gameobject.change_state(VENOM_IDLE)

    venom_gameobject.move(input)
    glutPostRedisplay()
    glutTimerFunc(20, timer_move_venom, 1)

def timer_animate_venom(value):
    global venom_gameobject
    venom_gameobject.animate()
    glutPostRedisplay()
    glutTimerFunc(100, timer_animate_venom, 1)

def timer_move_green_globin(value):
    global green_gameobject, w
    green_gameobject.automatic_move(w)
    glutPostRedisplay()
    glutTimerFunc(10, timer_move_green_globin, 1)

def timer_sound_green_globin(value):
    thread_sound_green = Thread(target=play_green)
    thread_sound_green.start()
    glutTimerFunc(10000, timer_sound_green_globin, 1)
#-------

def main():
    global texture_spiderman, spiderman_gameobject, texture_background, texture_platform
    global venom_gameobject, green_gameobject, texture_green_globin
    global GROUND
    glutInit (  )
    glutInitDisplayMode ( GLUT_RGBA )
    glutInitWindowSize ( w, h )
    glutInitWindowPosition( 0, 0 )
    
    glutCreateWindow( "Ventana de PyOpenGL" )
    glutDisplayFunc (display)
    #glutIdleFunc ( animate )
    glutReshapeFunc ( reshape )
    glutKeyboardFunc( keyPressed )
    glutKeyboardUpFunc(keyUp)
    init()

    texture_background = loadTexture('Resources/Background/fondo.png')
    texture_platform = loadTexture('Resources/Background/plataforma.png')

    texture_green_globin.append([loadTexture('Resources/GreenGlobin/green_globin.png')])
    green_gameobject = GameObject(0,400,(int)(174/3),(int)(122/3), texture_green_globin)

    texture_spiderman.append([loadTexture('Resources/Spiderman/spidermanidle.png')])
    texture_spiderman.append([loadTexture('Resources/Spiderman/spidermanrun1.png'),loadTexture('Resources/Spiderman/spidermanrun2.png'),loadTexture('Resources/Spiderman/spidermanrun3.png'),loadTexture('Resources/Spiderman/spidermanrun4.png'),loadTexture('Resources/Spiderman/spidermanrun5.png'),loadTexture('Resources/Spiderman/spidermanrun6.png'),loadTexture('Resources/Spiderman/spidermanrun7.png'),loadTexture('Resources/Spiderman/spidermanrun8.png')])
    texture_spiderman.append([loadTexture('Resources/Spiderman/spidermanjump.png')])
    spiderman_gameobject = GameObject(0,GROUND,(int)(226/4),(int)(282/4), texture_spiderman)

    texture_venom.append([loadTexture('Resources/Venom/venom_idle.png')])
    texture_venom.append([loadTexture('Resources/Venom/venom_run1.png'),loadTexture('Resources/Venom/venom_run2.png'),loadTexture('Resources/Venom/venom_run3.png'),loadTexture('Resources/Venom/venom_run4.png'),loadTexture('Resources/Venom/venom_run5.png'),loadTexture('Resources/Venom/venom_run6.png'),loadTexture('Resources/Venom/venom_run7.png'),loadTexture('Resources/Venom/venom_run8.png'),loadTexture('Resources/Venom/venom_run9.png'),loadTexture('Resources/Venom/venom_run10.png')])
    texture_venom.append([loadTexture('Resources/Venom/venom_jump.png')])
    venom_gameobject = GameObject(350,GROUND+8,(int)(300/5),(int)(339/5), texture_venom)

    timer_move_spiderman(0)
    timer_move_venom(0)
    timer_animate_spiderman(0)
    timer_animate_venom(0)
    timer_move_green_globin(0)
    timer_sound_green_globin(0)



    thread_sound = Thread(target=play_song)
    thread_sound.start()
    
    glutMainLoop()

print("Presiona Escape para cerrar.")
main()