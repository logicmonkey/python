import tkinter
import time
import random

with open('lm_bolokai.py') as f: exec(f.read())

def hilbert_s_to_xy(s, bits):
  x = 0
  y = 0

  for i in range(0, bits):
    sa = (s>>(2*i+1))&1
    sb = (s>>(2*i))&1
    if sa==sb:
      x, y = y, x
      if sa==1:
        x = ~x
        y = ~y

    if sa==1:
      x |= (1<<i) # set bit i
    else:
      x &= ~(1<<i) # clr bit i

    if sa==sb:
      y &= ~(1<<i) # clr bit i
    else:
      y |= (1<<i) # set bit i

  return x&((1<<bits)-1), y&((1<<bits)-1)

def hilbert_xy_to_s(x, y, bits):
  s = 0

  for i in reversed(range(0, 2**bits)):
    xs = (x>>i)&1;
    ys = (y>>i)&1;
    if ys==0:
      nxs = ~xs+1
      x, y = y^nxs, x^nxs

    s = (s<<2) | (xs<<1) | (xs^ys)

  return s

ORDER = 4
STEP  = int(110/ORDER)
DELAY = 0.01
XMAX = STEP*(2**ORDER)
YMAX = XMAX

# Event handler
def keypress(e):
  global done
  done = True
  return

# Main window
def create_window():
  window = tkinter.Tk()
  window.title("Hilbert")
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
      tvals=list(range(0, 2**(2*ORDER)))
      if mode==2:
        random.shuffle(tvals)
      for t in tvals:
        x, y = hilbert_s_to_xy(t, ORDER)
        x = STEP/2 + STEP*x
        y = STEP/2 + STEP*y

        if t != 2**(2*ORDER)-1: # don't draw beyond last point
          x_n, y_n = hilbert_s_to_xy(t+1, ORDER)
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
      yr = list(range(0,2**ORDER))
      xr = list(range(0,2**ORDER))
      if mode==3:
          random.shuffle(yr)
          random.shuffle(xr)
      for y in yr:
        for x in xr:
          s = hilbert_xy_to_s(x, y, ORDER)
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
