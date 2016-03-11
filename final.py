from math import *
from random import *
from tkinter import *
from collections import namedtuple

KEY_LEFT = 113
KEY_RIGHT = 114
KEY_UP = 111
KEY_DOWN = 116
KEY_SPACE = 65    

grid_size = 16

class Ent():
    x = 1
    y = 1
    face = 'r'
    
    def draw(self, canvas):
        print("you didnt implement this yet dumbass")
    def control(self, grid, key):
        print("not implemented")
        
class Dot(Ent):
    def draw(self, canvas):
        rads = 0
        if self.face == 'r': rads = 0
        if self.face == 'u': rads = pi/2
        if self.face == 'l': rads = pi
        if self.face == 'd': rads = 3*pi/2
        canvas.create_line((self.x+.5)*grid_size,
                           (self.y+.5)*grid_size,
                           (self.x+.5)*grid_size+1000*cos(rads+pi/4),
                           (self.y+.5)*grid_size-1000*sin(rads+pi/4),
                           dash=(4, 4))
        canvas.create_line((self.x+.5)*grid_size,
                           (self.y+.5)*grid_size,
                           (self.x+.5)*grid_size+1000*cos(rads-pi/4),
                           (self.y+.5)*grid_size-1000*sin(rads-pi/4),
                           dash=(4, 4))
        canvas.create_oval(self.x*grid_size, self.y*grid_size, (self.x+1)*grid_size, (self.y+1)*grid_size, fill = "red")

                           
    def control(self, grid, key):
        next_x = self.x
        next_y = self.y
        if key == KEY_LEFT: next_x -= 1
        if key == KEY_RIGHT: next_x += 1
        if key == KEY_UP: next_y -= 1
        if key == KEY_DOWN: next_y += 1

        if not grid[next_x][next_y]:
            if next_x > self.x: self.face = 'r'
            if next_x < self.x: self.face = 'l'
            if next_y > self.y: self.face = 'd'
            if next_y < self.y: self.face = 'u'
            self.x = next_x
            self.y = next_y
        
        pass


occupancy = []
class Box(Ent):
    def draw(self, canvas):
        rads = 0
        if self.face == 'r': rads = 0
        if self.face == 'u': rads = pi/2
        if self.face == 'l': rads = pi
        if self.face == 'd': rads = 3*pi/2
        canvas.create_line((self.x+.5)*grid_size,
                           (self.y+.5)*grid_size,
                           (self.x+.5)*grid_size+1000*cos(rads+pi/4),
                           (self.y+.5)*grid_size-1000*sin(rads+pi/4))
        canvas.create_line((self.x+.5)*grid_size,
                           (self.y+.5)*grid_size,
                           (self.x+.5)*grid_size+1000*cos(rads-pi/4),
                           (self.y+.5)*grid_size-1000*sin(rads-pi/4))
        canvas.create_rectangle(self.x*grid_size, self.y*grid_size, (self.x+1)*grid_size, (self.y+1)*grid_size, fill = "blue")
        
        
    def control(self, grid, key):
        next_x = self.x
        next_y = self.y

        if key == KEY_SPACE:
            reset_occupancy()
            occupancy[ents[0].x][ents[0].y] = 1
            #print(occupancy)
        else: 
            prev = []
            for x in range(0, grid_width-1):
                prev.append([])
                for y in range(0, grid_height):
                    prev[x].append(occupancy[x][y])
                    #occupancy[x][y] = 0
            for x in range(0, grid_width-1):
                for y in range(0, grid_height):
                    current = prev[x][y]
                    occupancy[x][y] -= current
                    positions = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                    valid = []
                    for pos in positions:
                        if not (\
                                pos[0] < 0 or pos[0] > grid_width-2 or \
                                pos[1] < 0 or pos[1] > grid_height-1 or \
                                grid[pos[0]][pos[1]]):
                            valid.append(pos)
                            amount = 0
                    if len(valid) > 0: amount = current/len(valid)
                    for pos in valid:
                        occupancy[pos[0]][pos[1]] += amount
                        #if amount > 0: print(occupancy[pos[0]][pos[1]])
        
        key = [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN]
        shuffle(key)
        key = key[0]
        
        
        if key == KEY_LEFT: next_x -= 1
        if key == KEY_RIGHT: next_x += 1
        if key == KEY_UP: next_y -= 1
        if key == KEY_DOWN: next_y += 1
        
        if not grid[next_x][next_y]:
            if next_x > self.x: self.face = 'r'
            if next_x < self.x: self.face = 'l'
            if next_y > self.y: self.face = 'd'
            if next_y < self.y: self.face = 'u'
            self.x = next_x
            self.y = next_y
        

ents = [Dot(), Box()]
grid_text = "\
##################################\n\
#         #                      #\n\
#                                #\n\
#                                #\n\
#                                #\n\
#                                #\n\
#                                #\n\
#                                #\n\
#                                #\n\
#                                #\n\
#                                #\n\
#                                #\n\
#                                #\n\
#                                #\n\
#                                #\n\
#                                #\n\
#                                #\n\
#                                #\n\
##################################\n"
grid_width = grid_text.index("\n")+1
grid_height = floor(len(grid_text)/grid_width)
grid = []
for x in range(0, grid_width-1):
    grid.append([])
    for y in range(0, grid_height):
        is_wall = False
        if grid_text[y*grid_width + x] == '#':
            is_wall = True
        grid[x].append(is_wall)


for x in range(0, grid_width-1):
    occupancy.append([])
    for y in range(0, grid_height):
        occupancy[x].append(0)
def reset_occupancy():
    for x in range(0, grid_width-1):
        for y in range(0, grid_height):
            occupancy[x][y] = 0
reset_occupancy()
        
master = Tk()

def gameFrame():

    """
    for ent in ents:
        ent.x = random()*10
        ent.y = random()*10
        pass
    """

    canvas.delete(ALL)

    for x in range(0, grid_width-1):
        for y in range(0, grid_height):
            alpha = occupancy[x][y]
            if alpha > 0:
                alpha = max(.05, min(1, alpha*10))

            alpha = floor(alpha*255)
            tk_rgb = "#%02x%02x%02x" % (255, 255-alpha, 255-alpha)
            #print(tk_rgb)
            #print(alpha)
            canvas.create_rectangle(x*grid_size, y*grid_size, (x+1)*grid_size, (y+1)*grid_size, fill=tk_rgb, outline=tk_rgb)
    
    for x in range(0, grid_width-1):
        for y in range(0, grid_height):
            if grid[x][y]:
                canvas.create_rectangle(x*grid_size, y*grid_size, (x+1)*grid_size, (y+1)*grid_size)
    

    for ent in ents:
        ent.draw(canvas)

    #master.after(floor(1000/60), gameFrame)

master.title("thingy")

w = 640
h = 480

toolbar = Frame(master, width=w, height=64)
toolbar.pack(side=BOTTOM)

canvas = Canvas(master, width=w, height=h)
canvas.pack(side=RIGHT)

def keyEvent(event):
    for ent in ents:
        ent.control(grid, event.keycode)

    #print(event.keycode)
    
    gameFrame()
    #print(event)

master.bind("<Key>", keyEvent)
gameFrame()

#master.after(floor(1000/60), gameFrame)
master.mainloop()
