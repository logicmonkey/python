################################################################################
#
#                           Pythagoras' Theorem
#
#                            b           a
#                        +-----------------------+
#                        |       /' .            |
#                        |      /     ' .        |b
#                        |     /          ' .    |
#                       a|    /c              ' .|
#                        |   /                  /|
#                        |  /                  / |
#                        | /                  /  |
#                      A_|/                  /   |
#                        |' .               /    |a
#                        |    ' .          /     |
#                       b|        ' .     /      |
#                        |            ' ./       |
#                        +-----------------------+
#                               a           b
#
#     A is a point on the left of the screen running from y=[0:height-1]
#     b is the remainder distance of the outer square of size a+b == height
#     sides a,b form a right angle triangle filled in blue
#
#     total area of the outer square is:
#
#         (a+b)^2 = a^2 + b^2 + 2ab
#
#     area c^2 is the total area minus the 4 corner triangles
#
#         c^2 = (a+b)^2 - 4(ab/2)
#
#     then
#
#         c^2 = a^2 + b^2
#                                                             -=LogicMonkey=-
################################################################################
import tkinter
import time

black = "#2e2e2e"
grey = "#797979"
white = "#d6d6d6"
yellow = "#e5b567"
green = "#b4d273"
orange = "#e87d3e"
purple = "#9e86c8"
pink = "#b05279"
blue = "#6c99bb"

DELTA = 2
DELAY = 0.01
XMAX = 240
YMAX = XMAX

# Main window
def create_window():
  window = tkinter.Tk()
  window.title("Pythagoras")
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
  direction = 1
  var_a = 1
  var_b = XMAX-1-var_a

  while True:
    # Draw everything
    canvas.create_rectangle(0, 0, var_a, var_a, outline=orange, fill=orange)
    canvas.create_rectangle(var_a, var_a, XMAX, XMAX, outline=blue, fill=blue)
    canvas.create_polygon(var_a, 0, 0, var_b, var_b, YMAX, XMAX, var_a, width=3, outline=green, fill='')

    window.update()
    time.sleep(DELAY)

    # Update coords and delete everything
    var_a += direction*DELTA
    var_b = XMAX-1-var_a
    if var_a >= XMAX or var_a <= 0:
      direction *= -1
      time.sleep(0.4)

    canvas.delete("all")

# Main
window = create_window()
canvas = create_canvas(window)
animate(window, canvas)
