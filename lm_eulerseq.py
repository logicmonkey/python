# +---------------------------+
# |         |                 |
# |         |                 |
# |         |                 |
# |   COS   |                 |
# |         |                 |
# |         |                 |
# |         |                 |
# |         |                 |
# |---------+-----------------|
# |         |  , ~ .          |
# | 5/6,5/6 | /     \         |
# |    o    |/       \  SIN  /|
# | PHASOR  |         \     / |
# |         |          ` _ '  |
# +-- 1/3 --------- 2/3 ------+
import tkinter
import time
import numpy as np

black = "#2e2e2e"
grey = "#797979"
white = "#d6d6d6"
yellow = "#e5b567"
green = "#b4d273"
orange = "#e87d3e"
purple = "#9e86c8"
pink = "#b05279"
blue = "#6c99bb"

R = 2 # dot radius
DELTA = 1
DELAY = 0.01
XMAX = 240
YMAX = XMAX
SCALE = 0.90
FREQ = 3
WIDTH = 2

# Main window
def create_window():
  window = tkinter.Tk()
  window.title('Euler\'s Eqn')
  window.geometry('{}x{}'.format(XMAX, YMAX))
  return window

# Create canvas and add to main window
def create_canvas(window):
  canvas = tkinter.Canvas(window)
  canvas.configure(bg=black)
  canvas.pack(fill="both", expand=True)
  return canvas

# Animation loop
def animate(window, canvas):
  # set initial coords
  xt = 0
  R=1
  while xt < 2*XMAX/3:
    sin = np.sin(2*np.pi*FREQ*xt/(2*XMAX/3)) * SCALE
    xpos_sin = XMAX/3 + xt
    ypos_sin = 5*YMAX/6 - YMAX/6 * sin

    cos = np.cos(2*np.pi*FREQ*xt/(2*XMAX/3)) * SCALE
    xpos_cos = XMAX/6 + XMAX/6*cos
    ypos_cos = 2*YMAX/3 - xt

    xpos_circ = XMAX/6 + XMAX/6*cos
    ypos_circ = 5*YMAX/6 - YMAX/6*sin

    canvas.create_oval(xpos_sin-R, ypos_sin-R, xpos_sin+R, ypos_sin+R, outline=purple, fill=purple)
    canvas.create_oval(xpos_cos-R, ypos_cos-R, xpos_cos+R, ypos_cos+R, outline=pink, fill=pink)
    canvas.create_oval(xpos_circ-R, ypos_circ-R, xpos_circ+R, ypos_circ+R, outline=green, fill=green)

    xt += 1/FREQ

  xt = 0

  while True:
    # Draw everything
    sin = np.sin(2*np.pi*FREQ*xt/(2*XMAX/3)) * SCALE
    xpos_sin = XMAX/3 + xt
    ypos_sin = 5*YMAX/6 - YMAX/6 * sin

    cos = np.cos(2*np.pi*FREQ*xt/(2*XMAX/3)) * SCALE
    xpos_cos = XMAX/6 + XMAX/6*cos
    ypos_cos = 2*YMAX/3 - xt

    xpos_circ = XMAX/6 + XMAX/6*cos
    ypos_circ = 5*YMAX/6 - YMAX/6*sin

    canvas.create_oval(xpos_sin-2*R, ypos_sin-2*R, xpos_sin+2*R, ypos_sin+2*R, outline=orange, fill=orange, tag='dots')
    canvas.create_oval(xpos_cos-2*R, ypos_cos-2*R, xpos_cos+2*R, ypos_cos+2*R, outline=orange, fill=orange, tag='dots')
    canvas.create_oval(xpos_circ-2*R, ypos_circ-2*R, xpos_circ+2*R, ypos_circ+2*R, outline=orange, fill=orange, tag='dots')

    canvas.create_line(xpos_circ, ypos_circ, xpos_sin, ypos_sin, width=WIDTH, fill=grey, tag='dots')
    canvas.create_line(xpos_circ, ypos_circ, xpos_cos, ypos_cos, width=WIDTH, fill=grey, tag='dots')
    canvas.create_line(XMAX/6, 5*YMAX/6, xpos_circ, ypos_circ, width=WIDTH, fill=grey, tag='dots')

    window.update()
    time.sleep(DELAY)

    # Update coords and delete everything
    xt += 1/FREQ

    canvas.delete("dots")

    if xt >= 2*XMAX/3:
        xt = 0
        time.sleep(0.5)

# Main
window = create_window()
canvas = create_canvas(window)
animate(window, canvas)
