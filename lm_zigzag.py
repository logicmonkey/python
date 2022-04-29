import tkinter
import time
import math
import random

with open('lm_bolokai.py') as f: exec(f.read())

def tri(n):
    return int(n*(n+1)/2) # Triangular number starts a diagonal

def tri_root(n):
    return int((math.sqrt(8*n+1)-1)/2)

def zz_s_to_xy(s, r): # distance s, reflection
    tr = tri_root(s)
    t = tri(tr) # nearest triangular number less than or equal to s
    d = s-t     # distance from the triangular start of diagonal
    if tr%2:    # check if the diagonal is an odd or even one
        if r:
            return ORDER-1-d, ORDER-1-tr+d
        else:
            return d, tr-d
    else:
        if r:
            return ORDER-1-tr+d, ORDER-1-d
        else:
            return tr-d, d

def zigzag_s_to_xy(s, ORDER):
    if (s<ORDER*ORDER/2): # left of main diagonal
        return zz_s_to_xy(s, 0)
    else:                 # right of main diagonal: reflect
        return zz_s_to_xy(ORDER**2-1-s, 1)

def zz_xy_to_s(x, y):
    # Even and odd diagonals increment in different directions
    if (x+y)%2:
        return tri(x+y) + x # for diagonals going up and right
    else:
        return tri(x+y) + y # for diagonals going down and left

def zigzag_xy_to_s(x, y, ORDER):
    if (x+y<ORDER): # left of main diagonal
        N = 0
        K = 1
        xt = x
        yt = y
    else:       # right of main diagonal: reflect
        N = ORDER*ORDER-1
        K = -1
        xt = ORDER-1 -x
        yt = ORDER-1 -y

    # distance s is purely a function of W, x and y
    return  N + K*zz_xy_to_s(xt, yt)

ORDER = 16
STEP  = int(110/math.sqrt(ORDER))
DELAY = 0.01
XMAX = STEP*ORDER
YMAX = XMAX

# Event handler
def keypress(e):
  global done
  done = True
  return

# Main window
def create_window():
  window = tkinter.Tk()
  window.title("Zig Zag")
  window.geometry('{}x{}'.format(XMAX, YMAX))
  window.bind("<Key>", keypress)
  return window

# Create canvas and add to main window
def create_canvas(window):
  canvas = tkinter.Canvas(window)
  canvas.configure(bg=darkgray)
  canvas.pack(fill="both", expand=True)
  return canvas

# Animation loop
def animate(window, canvas):
  # set initial coords
  s = 0
  mode = True

  while not done:

    if mode:
      tvals=list(range(0, ORDER**2))
      random.shuffle(tvals)
      for t in tvals:
        x, y = zigzag_s_to_xy(t, ORDER)
        x = STEP/2 + STEP*x
        y = STEP/2 + STEP*y

        if t != ORDER**2-1: # don't draw beyond last point
          x_n, y_n = zigzag_s_to_xy(t+1, ORDER)
          x_n = STEP/2 + STEP*x_n
          y_n = STEP/2 + STEP*y_n
          canvas.create_line(x, y, x_n, y_n, width=4, fill=brightpink, tag='line')

        window.update()
        time.sleep(DELAY)
        window.update()

      canvas.delete('line')
      time.sleep(80*DELAY)
      window.update()
      time.sleep(80*DELAY)
      mode = not mode

    else:
      for y in range(0, ORDER):
        for x in range(0, ORDER):
          s = zigzag_xy_to_s(x, y, ORDER)
          xs = STEP/2 + STEP*x
          ys = STEP/2 + STEP*y
          canvas.create_text(xs, ys, text=s, tag='text')

          window.update()
          time.sleep(DELAY)
          window.update()

      canvas.delete('text')
      mode = not mode

      time.sleep(20*DELAY)
      window.update()
      time.sleep(20*DELAY)

  window.destroy()

# Main
done = False
window = create_window()
canvas = create_canvas(window)
animate(window, canvas)
