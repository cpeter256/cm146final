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

    if occupancy_visible:
        for x in range(0, grid_width-1):
            for y in range(0, grid_height):
                alpha = state.occupancy[x][y]
                alpha *= 100
                if alpha == 0:
                    tk_rgb = "#dddddd"
                else:
                    if alpha > 1:
                        alpha -= 1
                        alpha *= 1/99
                        alpha = min(1, alpha*60)
                        alpha = floor(alpha*255)
                        tk_rgb = "#%02x%02x%02x" % (alpha, 0, 255-alpha)
                    else:
                        alpha *= 1
                        alpha = floor(alpha*255)
                        tk_rgb = "#%02x%02x%02x" % (255-alpha, 255-alpha, 255)
                    #print(tk_rgb)
                    #print(alpha)
                canvas.create_rectangle(x*grid_size, y*grid_size, (x+1)*grid_size, (y+1)*grid_size, fill=tk_rgb, outline=tk_rgb)
    
    for x in range(0, grid_width-1):
        for y in range(0, grid_height):
            if state.grid[x][y]:
                canvas.create_rectangle(x*grid_size, y*grid_size, (x+1)*grid_size, (y+1)*grid_size)
    

    for i in range(0, len(state.ents)):
        if i == 1 and not ai_visible:
            dx = state.ents[i].x-state.ents[0].x
            dy = state.ents[i].y-state.ents[0].y
            face = state.ents[0].face
            if (face == 'r' and abs(dy) > dx) or \
               (face == 'l' and abs(dy) > -dx) or \
               (face == 'u' and abs(dx) > -dy) or \
               (face == 'd' and abs(dx) > dy):
                continue

            if not los(state.ents[0].x, state.ents[0].y, state.ents[i].x, state.ents[i].y, state):
                continue
        state.ents[i].draw(state, canvas)

    #master.after(floor(1000/60), gameFrame)

master.title("thingy")

w = 640
h = 480
occupancy_visible = False
ai_visible = False
def toggle_occupancy():
    global occupancy_visible
    if occupancy_visible:
        occupancy_visible = False
    else:
        occupancy_visible = True
    gameFrame(game_state)

def toggle_aivis():
    global ai_visible
    if ai_visible:
        ai_visible = False
    else:
        ai_visible = True
    gameFrame(game_state)

    
toolbar = Frame(master, width=w, height=64)
occtog = Button(toolbar, text="toggle occupancy grid", command=toggle_occupancy)
occtog.pack()
aitog = Button(toolbar, text="toggle ai visibility", command=toggle_aivis)
aitog.pack()
toolbar.pack(side=BOTTOM)

canvas = Canvas(master, width=w, height=h)
canvas.pack(side=RIGHT)


def keyEvent(event):
    if game_state.player == 0:
        game_state.apply_move(game_state.ents[0], event.keysym)
        game_state.apply_move(game_state.ents[1], game_state.ents[1].decide(game_state))
    elif game_state.player == 1:
        game_state.apply_move(game_state.ents[1], event.keysym)
        game_state.apply_move(game_state.ents[0], game_state.ents[0].decide(game_state))
    else:
        game_state.apply_move(game_state.ents[0], game_state.ents[0].decide(game_state))
        game_state.apply_move(game_state.ents[1], game_state.ents[1].decide(game_state))

    #print(event.keysym)
    
    gameFrame(game_state)
    #print(event)
def mouseEvent(event):
    gx = int(floor(event.x/grid_size))
    gy = int(floor(event.y/grid_size))
    #los(game_state.ents[0].x, game_state.ents[0].y, gx, gy, game_state, canvas)

master.bind("<Key>", keyEvent)
master.bind("<Button-1>", mouseEvent)
gameFrame(game_state)

#master.after(floor(1000/60), gameFrame)
master.mainloop()
