import tkinter
import time
import random

N = 16

with open('lm_bolokai.py') as f: exec(f.read())

import math
SQREG = int(math.log(N,2))+2
STEP  = int(110/math.sqrt(N))
DELAY = 0.01
XMAX = STEP*N
YMAX = XMAX

def isqrt_pipe(arem, aval, stage):
    one = 1 << 2*stage
    cmp = aval | one

    yrem = arem
    yval = aval >> 1
    if arem >= cmp:
        yrem = yrem - cmp
        yval = yval | one
    return yrem, yval

def isqrt(n):
    rem = n
    val = 0
    for pp in reversed(range(0, SQREG)):
        rem, val = isqrt_pipe(rem, val, pp)
    return val

def tri(n):
    return (n*(n+1))>>1 # Triangular number starts a diagonal

def tri_root(n):
    return (isqrt(n<<3|1)-1)>>1

def zz_s_to_xy(s, rpd): # distance s, right of principal diagonal
    tr = tri_root(s)
    t = tri(tr) # nearest triangular number less than or equal to s
    d = s-t     # distance from the triangular start of diagonal
    if tr%2:    # check if the diagonal is an odd or even one
        if rpd: # right of principal diagonal
            return N-1-d, N-1-tr+d
        else:
            return d, tr-d
    else:
        if rpd:
            return N-1-tr+d, N-1-d
        else:
            return tr-d, d

def zigzag_s_to_xy(s, N):
    if (s<N*N/2): # left of main diagonal
        return zz_s_to_xy(s, 0)
    else:                 # right of main diagonal: reflect
        return zz_s_to_xy(N**2-1-s, 1)

def zz_xy_to_s(x, y):
    # Even and odd diagonals increment in different directions
    if (x+y)%2:
        return tri(x+y) + x # for diagonals going up and right
    else:
        return tri(x+y) + y # for diagonals going down and left

def zigzag_xy_to_s(x, y, N):
    if (x+y<N): # left of main diagonal
        END = 0
        K = 1
        xt = x
        yt = y
    else:       # right of main diagonal: reflect
        END = N*N-1
        K = -1
        xt = N-1 -x
        yt = N-1 -y

    # distance s is purely a function of W, x and y
    return  END + K*zz_xy_to_s(xt, yt)

# Event handler
def keypress(e):
  global done
  done = True
  return

# Main window
def create_window():
  window = tkinter.Tk()
  window.title("Zigzag")
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
  mode = 0

  while not done:

    if mode%2==0:
      tvals=list(range(0, N**2))
      if mode==2:
        random.shuffle(tvals)
      for t in tvals:
        x, y = zigzag_s_to_xy(t, N)
        x = STEP/2 + STEP*x
        y = STEP/2 + STEP*y

        if t != N**2-1: # don't draw beyond last point
          x_n, y_n = zigzag_s_to_xy(t+1, N)
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
      mode = mode + 1

    else:
      yr = list(range(0,N))
      xr = list(range(0,N))
      if mode==3:
          random.shuffle(yr)
          random.shuffle(xr)
      for y in yr:
        for x in xr:
          s = zigzag_xy_to_s(x, y, N)
          xs = STEP/2 + STEP*x
          ys = STEP/2 + STEP*y
          canvas.create_text(xs, ys, text=s, tag='text')

          window.update()
          time.sleep(DELAY)
          window.update()

      canvas.delete('text')
      mode = mode + 1
      if mode==4:
          mode = 0

      time.sleep(20*DELAY)
      window.update()
      time.sleep(20*DELAY)

  window.destroy()

# Main
done = False
window = create_window()
canvas = create_canvas(window)
animate(window, canvas)
