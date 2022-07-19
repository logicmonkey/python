#                                                      ,`\
#                                                 ...    /
#                                               @ o o @.'
#                                             .' ( o )
#                                            /  (     )
#                                            .'  \ : /
#                                               nnn nnn
import math
import tkinter
import random

ELEM  = 8
CX    = int(ELEM*math.log(ELEM,2)*(math.log(ELEM,2)+1)/4)

#    0   1   2   3   4   5   6   7
#
#    0---o-------o-------o--------
#        |       |       |
#    1---o-------|---o---o--------
#                |   |
#    2-------o---o---|-------o----
#            |       |       |
#    3-------o-------o-------o----
#

GRID = 40
BLOB = GRID>>3
XMAX = (CX+1)*GRID
YMAX = ELEM*GRID
XOFF = GRID
YOFF = GRID>>1

def bitonic_nodes(n):
    y = []
    for k in range(0, int(math.log(n, 2))): # 0:log(n)-1
        for j in range(k, -1, -1):         # k:0
            for i in range(0, n):          # 0:n-1
                l = i ^ (1<<j)             # invert bit j in i
                if (l > i):                # add low and high nodes
                    y += [i, l]            # in low, high order
    return y

# Main window
def create_window():
    window = tkinter.Tk()
    window.title('Bitonic Counting Network')
    window.geometry('{}x{}'.format(XMAX, YMAX))
    return window

# Create canvas and add to main window
def create_canvas(window):
    canvas = tkinter.Canvas(window)
    canvas.configure(bg=darkgray)
    canvas.pack(fill='both', expand=True)
    return canvas

def draw_network(window, canvas, nodes):

    color = pastelblue

    # create all horizontal lanes
    for y in range(0, ELEM):
        sx = 0
        sy = YOFF+GRID*y
        ex = XMAX
        ey = sy
        canvas.create_line(sx, sy, ex, ey, width=4, fill=color)

    # add routing nodes
    for x in range(0, CX):
        for y in range(0, ELEM):
            if (y == nodes[2*x]):
                sx = XOFF+GRID*x
                sy = YOFF+GRID*y
                ex = sx
                ey = YOFF+GRID*nodes[2*x+1]
                canvas.create_line(sx, sy, ex, ey, width=4, fill=color)
                canvas.create_oval(sx-BLOB, sy-BLOB, sx+BLOB, sy+BLOB, width=BLOB, outline=color, fill=color)
                canvas.create_oval(ex-BLOB, ey-BLOB, ex+BLOB, ey+BLOB, width=BLOB, outline=color, fill=color)

# Main
with open('lm_bolokai.py') as f: exec(f.read())
COLOR = [pastelblue, pastelyellow, pastelpurple, pastelgreen, pastelpink,
        darkred, darkgreen, darkblue, brightgreen, darkmagenta, darkwhite, black]

window = create_window()
canvas = create_canvas(window)
nodes = bitonic_nodes(ELEM)
random_mode = False

invec = ELEM*[0]
invec[0] = 1
#invec[1] = 1

draw_network(window, canvas, nodes)

vec = invec
state = CX*[0]

i=""
while (i!='x' and i!='q'):
    color = pastelyellow
    for x in range(0, CX):

        # draw the lead in path for aesthetic purposes
        for y in range(0, ELEM):
            if (invec[y]==1):
                sx = 0
                sy = YOFF+GRID*y
                ex = GRID
                ey = sy
                canvas.create_line(sx, sy, ex, ey, width=4, fill=color)

        # simulate the counting network
        vec_nxt = ELEM*[0]

        for y in range(0, ELEM):
            if (vec[y]==1):
                sx = XOFF+GRID*x
                sy = YOFF+GRID*y

                # upper path
                if (y==nodes[2*x]) and (state[x]==0):
                    vec_nxt[y] = 1
                    state[x] = 1
                    ex = XOFF+GRID*(x+1)
                    ey = sy

                # down and right
                elif (y==nodes[2*x]) and (state[x]==1):
                    vec_nxt[nodes[2*x+1]] = 1
                    state[x] = 0
                    ex = sx
                    ey = YOFF+GRID*nodes[2*x+1]
                    canvas.create_line(sx, sy, ex, ey, width=4, fill=color)
                    sx = ex
                    sy = ey
                    ex = XOFF+GRID*(x+1)
                    ey = ey

                # lower path
                elif (y==nodes[2*x+1]) and (state[x]==1):
                    vec_nxt[y] = 1
                    state[x] = 0
                    ex = XOFF+GRID*(x+1)
                    ey = sy

                # up and right
                elif (y==nodes[2*x+1]) and (state[x]==0):
                    vec_nxt[nodes[2*x]] = 1
                    state[x] = 1
                    ex = sx
                    ey = YOFF+GRID*nodes[2*x]
                    canvas.create_line(sx, sy, ex, ey, width=4, fill=color)
                    sx = ex
                    sy = ey
                    ex = XOFF+GRID*(x+1)
                    ey = ey

                # no node
                else:
                    vec_nxt[y] = 1
                    ex = XOFF+GRID*(x+1)
                    ey = sy

        vec = vec_nxt
        canvas.create_line(sx, sy, ex, ey, width=4, fill=color)
    i=input('>')
    if (i=='r'):
        random_mode = not random_mode
    if random_mode:
        random.shuffle(invec)
    vec = invec
    draw_network(window, canvas, nodes)

window.destroy()
