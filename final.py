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

def distance(x1, y1, x2, y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)


def los(x1, y1, x2, y2, canvas = None):
    cx = x1
    cy = y1
    dx = x2-x1
    dy = y2-y1
    dist = sqrt((x2-x1)**2 + (y2-y1)**2)

    if dist == 0: return True

    dx /= dist
    dy /= dist

    if dx == 0:
        while cy != y2:
            cy += dy
            if grid[int(cx)][int(cy)]:
                return False
        return True
    elif dy == 0:
        while cx != x2:
            cx += dx
            if grid[int(cx)][int(cy)]:
                return False
        return True
    else:
        islope = dy/dx
        slope = dx/dy

        hdir = 1
        if dx < 0: hdir = -1
        vdir = 1
        if dy < 0: vdir = -1

        cx += .5
        cy += .5

        col = "blue"
        
        while distance(x1+.5, y1+.5, cx, cy) < dist:
            hdist = 0
            if hdir > 0:
                hdist = floor(cx+1)-cx
            else:
                hdist = ceil(cx-1)-cx
            hor = (cx+hdist, cy+hdist*islope)
            vdist = 0
            if vdir > 0:
                vdist = floor(cy+1)-cy
            else:
                vdist = ceil(cy-1)-cy
            ver = (cx+vdist*slope, cy+vdist)
            nxt = ver
            if distance(cx, cy, hor[0], hor[1]) < distance(cx, cy, ver[0], ver[1]):
                nxt = hor
            middle = ((cx+nxt[0])/2, (cy+nxt[1])/2)
            coord = (int(floor(middle[0])), int(floor(middle[1])))

            
            if canvas != None:
                canvas.create_line(cx*grid_size, cy*grid_size, nxt[0]*grid_size, nxt[1]*grid_size, fill=col)
                if col == "blue":
                    col = "yellow"
                else:
                    col = "blue"

            if grid[coord[0]][coord[1]]:
                return False

            cx = nxt[0]
            cy = nxt[1]
        return True


def valid_coord(x, y):
    return not (\
                x < 0 or x > grid_width-2 or \
                y < 0 or y > grid_height-1 or \
                grid[x][y])
                           

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

        if key == KEY_SPACE: # or True:
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

        consumed = 0
        for depth in range(0, 999):
            if self.face == 'r' and self.x+depth > grid_width-2:
                break
            if self.face == 'l' and self.x-depth < 0:
                break
            if self.face == 'u' and self.y-depth < 0:
                break
            if self.face == 'd' and self.y+depth > grid_height-1:
                break
            
            for lat in range(-depth, depth+1):
                cx = 0
                cy = 0
                if self.face == 'r':
                    cx = self.x+depth
                    cy = self.y+lat
                if self.face == 'l':
                    cx = self.x-depth
                    cy = self.y+lat
                if self.face == 'u':
                    cy = self.y-depth
                    cx = self.x+lat
                if self.face == 'd':
                    cy = self.y+depth
                    cx = self.x+lat

                #print(str(cx) + " " + str(cy))
                if valid_coord(cx, cy):
                    if los(self.x, self.y, cx, cy):
                        consumed += occupancy[cx][cy]
                        occupancy[cx][cy] = 0
                        pass

        total = 1-consumed
        for x in range(0, grid_width-1):
            for y in range(0, grid_height):
                if total > 0:
                    occupancy[x][y] /= total
                else:
                    occupancy[x][y] = 0

        if los(self.x, self.y, ents[0].x, ents[0].y):
            dx = ents[0].x-self.x
            dy = ents[0].y-self.y
            if (self.face == 'r' and abs(dy) <= dx) or \
               (self.face == 'l' and abs(dy) <= -dx) or \
               (self.face == 'u' and abs(dx) <= -dy) or \
               (self.face == 'd' and abs(dx) <= dy):
                reset_occupancy()
                occupancy[ents[0].x][ents[0].y] = 1


                    
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

        if los(self.x, self.y, ents[0].x, ents[0].y):
            dx = ents[0].x-self.x
            dy = ents[0].y-self.y
            if (self.face == 'r' and abs(dy) <= dx) or \
               (self.face == 'l' and abs(dy) <= -dx) or \
               (self.face == 'u' and abs(dx) <= -dy) or \
               (self.face == 'd' and abs(dx) <= dy):
                reset_occupancy()
                occupancy[ents[0].x][ents[0].y] = 1


ents = [Dot(), Box()]
grid_text = "\
##################################\n\
#         #                #     #\n\
#         #                #     #\n\
#      ####   ######       #     #\n\
#             #            #     #\n\
#             #    #       #     #\n\
#      ########    #             #\n\
#         #        #             #\n\
#         #    ###############   #\n\
#   #######    #             #   #\n\
#   #     #    #             #   #\n\
#   #          #             #   #\n\
#   #          #             #   #\n\
#   ############             #   #\n\
#                          ###   #\n\
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
def mouseEvent(event):
    gx = int(floor(event.x/grid_size))
    gy = int(floor(event.y/grid_size))
    los(ents[0].x, ents[0].y, gx, gy, canvas)

master.bind("<Key>", keyEvent)
master.bind("<Button-1>", mouseEvent)
gameFrame()

#master.after(floor(1000/60), gameFrame)
master.mainloop()
