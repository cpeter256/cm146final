from math import *
from random import *
from tkinter import *
from collections import namedtuple

KEY_LEFT = 113
KEY_RIGHT = 114
KEY_UP = 111
KEY_DOWN = 116
    

grid_size = 16

class Ent():
    x = 1
    y = 1
    
    def draw(self, canvas):
        print("you didnt implement this yet dumbass")
    def control(self, grid, key):
        print("not implemented")
        
class Dot(Ent):
    def draw(self, canvas):
        canvas.create_oval(self.x*grid_size, self.y*grid_size, (self.x+1)*grid_size, (self.y+1)*grid_size, fill = "red")

    def control(self, grid, key):
        next_x = self.x
        next_y = self.y
        if key == KEY_LEFT: next_x -= 1
        if key == KEY_RIGHT: next_x += 1
        if key == KEY_UP: next_y -= 1
        if key == KEY_DOWN: next_y += 1

        if not grid[next_x][next_y]:
            self.x = next_x
            self.y = next_y
        
        pass

class Box(Ent):
    def draw(self, canvas):
        canvas.create_rectangle(self.x*grid_size, self.y*grid_size, (self.x+1)*grid_size, (self.y+1)*grid_size, fill = "blue")

    def control(self, grid, key):
        next_x = self.x
        next_y = self.y

        key = [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN]
        shuffle(key)
        key = key[0]
        
        
        if key == KEY_LEFT: next_x -= 1
        if key == KEY_RIGHT: next_x += 1
        if key == KEY_UP: next_y -= 1
        if key == KEY_DOWN: next_y += 1

        if not grid[next_x][next_y]:
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
    
    gameFrame()
    #print(event)

master.bind("<Key>", keyEvent)
gameFrame()

#master.after(floor(1000/60), gameFrame)
master.mainloop()
