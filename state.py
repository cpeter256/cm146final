from math import *
from random import *
from collections import namedtuple, Counter

KEY_LEFT = "Left"
KEY_RIGHT = "Right"
KEY_UP = "Up"
KEY_DOWN = "Down"
KEY_SPACE = "space"

grid_size = 16

def distance(x1, y1, x2, y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)


def los(x1, y1, x2, y2, state, canvas = None):
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
            if state.grid[int(cx)][int(cy)]:
                return False
        return True
    elif dy == 0:
        while cx != x2:
            cx += dx
            if state.grid[int(cx)][int(cy)]:
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

            if state.grid[coord[0]][coord[1]]:
                return False

            cx = nxt[0]
            cy = nxt[1]
        return True


def valid_coord(x, y, state):
    return not (\
                x < 0 or x > grid_width-2 or \
                y < 0 or y > grid_height-1 or \
                state.grid[x][y])
                           

class Ent():
    x = 1
    y = 1
    face = 'r'
    
    def draw(self, state, canvas):
        print("you didnt implement this yet dumbass")
    def control(self, state, key):
        print("not implemented")
        
class Dot(Ent):
    def draw(self, state, canvas):
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

                           
    def control(self, state, key):
        next_x = self.x
        next_y = self.y
        if key == KEY_LEFT: next_x -= 1
        if key == KEY_RIGHT: next_x += 1
        if key == KEY_UP: next_y -= 1
        if key == KEY_DOWN: next_y += 1

        if not state.grid[next_x][next_y]:
            if next_x > self.x: self.face = 'r'
            if next_x < self.x: self.face = 'l'
            if next_y > self.y: self.face = 'd'
            if next_y < self.y: self.face = 'u'
            self.x = next_x
            self.y = next_y
        
        pass



class Box(Ent):
    def draw(self, state, canvas):
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
        
        
    def control(self, state, key):
        next_x = self.x
        next_y = self.y

        if False: # key == KEY_SPACE: # or True:
            state.reset_occupancy()
            state.occupancy[state.ents[0].x][state.ents[0].y] = 1
            #print(occupancy)
        else: 
            prev = []
            for x in range(0, grid_width-1):
                prev.append([])
                for y in range(0, grid_height):
                    prev[x].append(state.occupancy[x][y])
                    #occupancy[x][y] = 0
            for x in range(0, grid_width-1):
                for y in range(0, grid_height):
                    current = prev[x][y]
                    state.occupancy[x][y] -= current
                    positions = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                    valid = []
                    for pos in positions:
                        if not (\
                                pos[0] < 0 or pos[0] > grid_width-2 or \
                                pos[1] < 0 or pos[1] > grid_height-1 or \
                                state.grid[pos[0]][pos[1]]):
                            valid.append(pos)
                            amount = 0
                    if len(valid) > 0: amount = current/len(valid)
                    for pos in valid:
                        state.occupancy[pos[0]][pos[1]] += amount
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
                if valid_coord(cx, cy, state):
                    if los(self.x, self.y, cx, cy, state):
                        consumed += state.occupancy[cx][cy]
                        state.occupancy[cx][cy] = 0
                        pass

        total = 1-consumed
        for x in range(0, grid_width-1):
            for y in range(0, grid_height):
                if total > 0:
                    state.occupancy[x][y] /= total
                else:
                    state.occupancy[x][y] = 0

        if los(self.x, self.y, state.ents[0].x, state.ents[0].y, state):
            dx = state.ents[0].x-self.x
            dy = state.ents[0].y-self.y
            if (self.face == 'r' and abs(dy) <= dx) or \
               (self.face == 'l' and abs(dy) <= -dx) or \
               (self.face == 'u' and abs(dx) <= -dy) or \
               (self.face == 'd' and abs(dx) <= dy):
                state.reset_occupancy()
                state.occupancy[state.ents[0].x][state.ents[0].y] = 1

                #TODO do the rest
                    
        key = [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN]
        shuffle(key)
        key = key[0]
        
        
        if key == KEY_LEFT: next_x -= 1
        if key == KEY_RIGHT: next_x += 1
        if key == KEY_UP: next_y -= 1
        if key == KEY_DOWN: next_y += 1
        
        if not state.grid[next_x][next_y]:
            if next_x > self.x: self.face = 'r'
            if next_x < self.x: self.face = 'l'
            if next_y > self.y: self.face = 'd'
            if next_y < self.y: self.face = 'u'
            self.x = next_x
            self.y = next_y

        if los(self.x, self.y, state.ents[0].x, state.ents[0].y, state):
            dx = state.ents[0].x-self.x
            dy = state.ents[0].y-self.y
            if (self.face == 'r' and abs(dy) <= dx) or \
               (self.face == 'l' and abs(dy) <= -dx) or \
               (self.face == 'u' and abs(dx) <= -dy) or \
               (self.face == 'd' and abs(dx) <= dy):
                state.reset_occupancy()
                state.occupancy[state.ents[0].x][state.ents[0].y] = 1

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

class State:
    def __init__(self):
        self.turn = "player"
        self.ents = [Dot(), Box()]
        self.occupancy = []
        self.grid = []
        for x in range(0, grid_width-1):
            self.grid.append([])
            for y in range(0, grid_height):
                is_wall = False
                if grid_text[y*grid_width + x] == '#':
                    is_wall = True
                self.grid[x].append(is_wall)

        for x in range(0, grid_width-1):
            self.occupancy.append([])
            for y in range(0, grid_height):
                self.occupancy[x].append(0)
        self.reset_occupancy()

    def reset_occupancy(self):
        for x in range(0, grid_width-1):
            for y in range(0, grid_height):
                self.occupancy[x][y] = 0


    def copy(self):
        temp = State()
        temp.turn = self.turn
        temp.ents = self.ents
        temp.occupancy = []
        temp.grid = []
        for x in range(0, grid_width-1):
            self.grid.append([])
            for y in range(0, grid_height):
                is_wall = False
                if grid_text[y*grid_width + x] == '#':
                    is_wall = True
                self.grid[x].append(is_wall)
        for x in range(0, grid_width-1):
            temp.occupancy.append([])
            for y in range(0, grid_height):
                temp.occupancy[x].append(self.occupancy[x][y])

        return temp
        
    def apply_move(self, target, move):
        inputs = ["Up", "Down", "Left", "Right"]
        if move not in inputs:
            move = "Stay"
        if move in self.legal_moves(target):
            target.control(self, move)


    def legal_moves(self, target):
        x = target.x
        y = target.y
        positions = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        valid = []
        valid.append("Stay")
        for pos in positions:
            if not (\
                pos[0] < 0 or pos[0] > grid_width-2 or \
                pos[1] < 0 or pos[1] > grid_height-1 or \
                self.grid[pos[0]][pos[1]]):
                if pos == (x+1, y):
                    valid.append("Right")
                elif pos == (x-1, y):
                    valid.append("Left")
                elif pos == (x, y+1):
                    valid.append("Down")
                elif pos == (x, y-1):
                    valid.append("Up")
        return valid

