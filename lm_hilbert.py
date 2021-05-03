import tkinter
import time

with open('lm_bolokai.py') as f: exec(f.read())

def hilbert_s_to_xy(s, bits):
  x = 0
  y = 0

  for i in range (0, bits):
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
  return 123

ORDER = 4
STEP  = int(100/ORDER)
DELAY = 0.02
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
  xlast = STEP/2
  ylast = STEP/2
  t = 0
  s = 0
  mode = False

  while not done:

    if mode:
      x, y = hilbert_s_to_xy(t, ORDER)
      x = STEP/2 + STEP*x
      y = STEP/2 + STEP*y

      canvas.create_line(xlast, ylast, x, y, width=4, fill=brightpink, tag='line')

      window.update()
      time.sleep(DELAY)
      window.update()

      xlast = x
      ylast = y

      t += 1
      if t == 2**(2*ORDER):
        xlast = STEP/2
        ylast = STEP/2
        t=0
        canvas.delete('line')
        mode = not mode

    else:
      for y in range(0, 2**ORDER):
        for x in range(0, 2**ORDER):
          s = hilbert_xy_to_s(x, y, ORDER)
          xs = STEP/2 + STEP*x
          ys = STEP/2 + STEP*y
          canvas.create_text(xs, ys, text=s, tag='text')

          window.update()
          time.sleep(DELAY)
          window.update()

      canvas.delete('text')
      mode = not mode

  window.destroy()

# Main
done = False
window = create_window()
canvas = create_canvas(window)
animate(window, canvas)
