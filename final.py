from math import *
from random import *
from tkinter import *
from state import *
from collections import namedtuple
#Global Game State
game_state = State()
        
master = Tk()

def gameFrame(state):

    """
    for ent in ents:
        ent.x = random()*10
        ent.y = random()*10
        pass
    """

    canvas.delete(ALL)

    for x in range(0, grid_width-1):
        for y in range(0, grid_height):
            alpha = state.occupancy[x][y]
            alpha *= 100
            if alpha == 0:
                tk_rgb = "#ffffff"
            else:
                if alpha > 5:
                    alpha -= 5
                    alpha *= 1/95
                    alpha = floor(alpha*255)
                    tk_rgb = "#%02x%02x%02x" % (alpha, 0, 255-alpha)
                else:
                    alpha *= 1/5
                    alpha = floor(alpha*255)
                    tk_rgb = "#%02x%02x%02x" % (255-alpha, 255-alpha, 255)
            #print(tk_rgb)
            #print(alpha)
            canvas.create_rectangle(x*grid_size, y*grid_size, (x+1)*grid_size, (y+1)*grid_size, fill=tk_rgb, outline=tk_rgb)
    
    for x in range(0, grid_width-1):
        for y in range(0, grid_height):
            if state.grid[x][y]:
                canvas.create_rectangle(x*grid_size, y*grid_size, (x+1)*grid_size, (y+1)*grid_size)
    

    for ent in state.ents:
        ent.draw(state, canvas)

    #master.after(floor(1000/60), gameFrame)

master.title("thingy")

w = 640
h = 480

toolbar = Frame(master, width=w, height=64)
toolbar.pack(side=BOTTOM)

canvas = Canvas(master, width=w, height=h)
canvas.pack(side=RIGHT)


def keyEvent(event):
    for ent in game_state.ents:
        game_state.apply_move(ent, event.keysym)

    #print(event.keysym)
    
    gameFrame(game_state)
    #print(event)
def mouseEvent(event):
    gx = int(floor(event.x/grid_size))
    gy = int(floor(event.y/grid_size))
    los(game_state.ents[0].x, game_state.ents[0].y, gx, gy, game_state, canvas)

master.bind("<Key>", keyEvent)
master.bind("<Button-1>", mouseEvent)
gameFrame(game_state)

#master.after(floor(1000/60), gameFrame)
master.mainloop()
