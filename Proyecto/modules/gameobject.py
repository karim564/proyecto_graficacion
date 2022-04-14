from telnetlib import GA


class GameObject:
    

    def __init__(self, x=0, y=0, w=0, h=0, frames = []):
        self.__position = {'x': 0, 'y': 0}
        self.__last_position = {'x': 0, 'y': 0}
        self.__size = {'x': 0, 'y': 0}
        self.animator = [] #Lista bidimensional con los frames del objeto
        self.__index_state = 0 #Indice del estado del personaje
        self.__latest_frame = 0 #Indice del frame a dibujar
        self.__mirror = False #mirror es falso cuando voltea hacia la derecha
        self.__velocity= {'x':0, 'y':0}
        self.__MAX_VELOCITY = 10
        self.__jumping = False

        self.__position['x'] = x
        self.__position['y'] = y
        self.__size['x'] = w
        self.__size['y'] = h
        self.animator = frames

    def automatic_move(self, scr_w):
        if self.__velocity['x'] == 0:
            self.__velocity['x'] = 3
        
        self.__position['x'] += self.__velocity['x']

        #Ver si colisiona con la pantalla
        if self.__position['x'] + self.__size['x'] > scr_w:
            self.__position['x'] = scr_w - self.__size['x']
            self.__velocity['x'] *= -1
        if self.__position['x']  < 0:
            self.__position['x'] = 0
            self.__velocity['x'] *= -1

    def move(self, input):
        '''Input:
        1.- Mover hacia la derecha
        0.- No se mueve
        -1.- Mover hacia la izquierda'''
        gravity = -0.25
        deltaT = 3

        if not self.__jumping and input['y'] == 1:
            self.__jumping = True
            self.__velocity['y'] = self.__MAX_VELOCITY

        if self.__jumping:
            self.__velocity['y'] += gravity*deltaT
            if self.__velocity['y'] < -self.__MAX_VELOCITY:
                self.__velocity['y'] = -self.__MAX_VELOCITY
            self.__last_position['y'] = self.__position['y']
            self.__position['y'] += self.__velocity['y']*deltaT
            if self.__position['y'] <= 50:
                self.__position['y'] = 50
                self.__jumping = False
                self.__velocity['y'] = 0

        if input['x'] == 0:
            if self.__velocity['x'] != 0:
                self.__velocity['x'] -= 0.1*self.__velocity['x']
            if abs(self.__velocity['x']) < 0.01:
                self.__velocity['x'] = 0
        else:
            if self.__position['x'] > 955:
                self.__velocity['x'] = 0
                self.__position['x'] = 955
            elif self.__position['x'] < 0:
                self.__velocity['x'] = 0
                self.__position['x'] = 0
            else:
                self.__velocity['x'] = self.__position['x'] - self.__last_position['x'] + input['x']
                if self.__velocity['x'] > self.__MAX_VELOCITY:
                    self.__velocity['x'] = self.__MAX_VELOCITY
                if self.__velocity['x'] < -self.__MAX_VELOCITY:
                    self.__velocity['x'] = -self.__MAX_VELOCITY

        self.__last_position['x'] = self.__position['x']
        self.__position['x'] += self.__velocity['x'] 

    def is_collision(self, obj):
        if not isinstance(obj, GameObject):
            raise Exception("Error")
        col_x = self.__position['x'] < obj.__position['x'] + obj.__size['x'] and self.__position['x'] + self.__size['x'] > obj.__position['x']
        col_y = self.__position['y'] < obj.__position['y'] + obj.__size['y'] and self.__position['y'] + self.__size['y'] > obj.__position['y']
        return col_x and col_y

    def change_state(self, index):
        if index >= len(self.animator):
            raise Exception('El indice está fuera del limite permitido.')
        self.__index_state = index
        self.__latest_frame = 0

    def animate(self):
        if len(self.animator[self.__index_state]) == 1:
            return
        self.__latest_frame = 0 if self.__latest_frame >= (len(self.animator[self.__index_state])-1) else self.__latest_frame +1
    
    def get_frame_to_draw(self):
        return self.animator[self.__index_state][self.__latest_frame]
        
    def get_position(self):
        return self.__position['x'], self.__position['y']
    
    def get_position_x(self):
        return self.__position['x']

    def get_size(self):
        return self.__size['x'], self.__size['y']

    def get_size_x(self):
        return self.__size['x']

    def get_state(self):
        return self.__index_state

    def set_mirror(self, value):
        self.__mirror = value
    
    def is_mirrored(self):
        return self.__mirror
    
    def get_velocity(self):
        return self.__velocity
    
    def set_velocity(self, value):
        self.__velocity = value