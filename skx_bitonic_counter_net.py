#  Copyright 2022 Piers Barber
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  SPDX-License-Identifier: Apache-2.0
#
#  0---o-------o-------o--------                                 ,`\
#      |       |       |                                    ...    /
#  1---o-------|---o---o--------                          @ o o @.'
#              |   |     piers.barber@logicmonkey.co.uk .' ( o )
#  2-------o---o---|-------o----                       /  (     )
#          |       |       |  Bitonic Counting Network \.' \ : /
#  3-------o-------o-------o----                          nnn nnn
import math
import tkinter

ELEM  = 8
# compare/exchange operations in a bitonic sorter network
CX    = int(ELEM*math.log(ELEM,2)*(math.log(ELEM,2)+1)/4)

GRID = 40
BLOB = GRID>>3
XMAX = (CX+1)*GRID
YMAX = ELEM*GRID
XOFF = GRID
YOFF = GRID>>1

# Define the network nodes in an array/list
# My bitonic sorter node calculation is an improvement on Wikipedia's
def bitonic_nodes(n):
    y = []
    for k in range(0, int(math.log(n,2))): # 0:log(n)-1
        for j in range(k, -1, -1):         # k:0
            for i in range(0, n):          # 0:n-1
                l = i ^ (1<<j)             # invert bit j in i
                if l > i:                  # add low and high nodes
                    y += [i, l]            # in low, high order
    return y

# My custom colour scheme and its crazy names
white        = "#f8f8f2"
darkwhite    = "#d6d6d6"
gray         = "#797979"
darkgray     = "#2e2e2e"
black        = "#000000"
pastelpurple = "#9e86c8"

pastelblue   = "#6c99bb"
brightblue   = "#66d9ef"
blue         = "#03b6fc"
darkcyan     = "#4694a3"
darkblue     = "#0281b3"
brightpurple = "#ae81ff"

pastelyellow = "#e5b567"
pastelorange = "#e87d3e"
brightorange = "#fd971f"
darkyellow   = "#b36b16"
pastelgreen  = "#b4d273"
darkgreen    = "#70991f"

pastelpink   = "#b05279"
brightpink   = "#f92672"
red          = "#f9263f"
darkmagenta  = "#b31b52"
darkred      = "#b31b1d"
brightgreen  = "#a6e22e"

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

    color = gray

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

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
COLOR = [black, pastelyellow, pastelorange, pastelgreen, pastelpink,
        darkred, pastelblue, darkwhite, brightgreen]

window = create_window()
canvas = create_canvas(window)
nodes = bitonic_nodes(ELEM)
draw_network(window, canvas, nodes)

invec = [1,2,3,4,5,6,7,8] # non-zero are active lane inputs

vec = invec
state = CX*[0]

instr = ''
while instr != 'x' and instr != 'q':

    # -------------------------------------------------------------------------
    # Simulate the counting network
    # -------------------------------------------------------------------------

    # loop over all columns and all lanes in each column
    for x in range(0, CX):

        # draw the lead in path for aesthetic purposes
        for y in range(0, ELEM):
            if invec[y] != 0:
                sx = 0
                sy = YOFF+GRID*y
                ex = GRID
                ey = sy
                canvas.create_line(sx, sy, ex, ey, width=4, fill=COLOR[invec[y]])

        vec_nxt = ELEM*[0] # start with a clear forwarded vector

        for y in range(0, ELEM):
            if vec[y] != 0:           # an active input
                sx = XOFF+GRID*x
                sy = YOFF+GRID*y

                # upper path
                if y==nodes[2*x] and state[x]==0 and vec[nodes[2*x+1]]==0:
                    vec_nxt[y] = vec[y]
                    state[x] = 1
                    ex = XOFF+GRID*(x+1)
                    ey = sy
                    canvas.create_line(sx, sy, ex, ey, width=4, fill=COLOR[vec[y]])

                # down and right
                elif y==nodes[2*x] and state[x]!=0 and vec[nodes[2*x+1]]==0:
                    vec_nxt[nodes[2*x+1]] = vec[y]
                    state[x] = 0
                    ex = sx
                    ey = YOFF+GRID*nodes[2*x+1]
                    canvas.create_line(sx, sy, ex, ey, width=4, fill=COLOR[vec[y]])
                    sx = ex
                    sy = ey
                    ex = XOFF+GRID*(x+1)
                    ey = ey
                    canvas.create_line(sx, sy, ex, ey, width=4, fill=COLOR[vec[y]])

                # lower path
                elif y==nodes[2*x+1] and state[x]!=0 and vec[nodes[2*x]]==0:
                    vec_nxt[y] = vec[y]
                    state[x] = 0
                    ex = XOFF+GRID*(x+1)
                    ey = sy
                    canvas.create_line(sx, sy, ex, ey, width=4, fill=COLOR[vec[y]])

                # up and right
                elif y==nodes[2*x+1] and state[x]==0 and vec[nodes[2*x]]==0:
                    vec_nxt[nodes[2*x]] = vec[y]
                    state[x] = 1
                    ex = sx
                    ey = YOFF+GRID*nodes[2*x]
                    canvas.create_line(sx, sy, ex, ey, width=4, fill=COLOR[vec[y]])
                    sx = ex
                    sy = ey
                    ex = XOFF+GRID*(x+1)
                    ey = ey
                    canvas.create_line(sx, sy, ex, ey, width=4, fill=COLOR[vec[y]])

                # either node contention or no node (no state change, pass through)
                else:
                    vec_nxt[y] = vec[y]
                    ex = XOFF+GRID*(x+1)
                    ey = sy
                    canvas.create_line(sx, sy, ex, ey, width=4, fill=COLOR[vec[y]])
        vec = vec_nxt

    # User interfaces bore me to tears: junk in -> error
    instr=input('>')
    if instr == 'v':
        inp = input('input vector \n8 lane ex: 1 2 0 0 3 4 0 0 \n> ')
        invec = list(map(int, inp.split()))
    if instr == 'r':
        state = CX*[0]
    if instr == 's':
        print(state)
    if instr == 'h':
        print(' <RTN> - advance\n   h   - this help\n   r   - reset state \n   v   - input vector\n   s   - show state\n  x|q  - exit')
    vec = invec
    draw_network(window, canvas, nodes)

window.destroy()
