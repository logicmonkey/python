import tkinter

with open('lm_bolokai.py') as f: exec(f.read())

COLS=2
ROWS=int(len(BOLOKAI)/COLS) # 6x4

WIDTH=80
HEIGHT=60
XMAX=COLS*WIDTH
YMAX=ROWS*HEIGHT

# Event handler
def keypress(event):
    global done
    done = True
    return

# Main window
def create_window():
  window = tkinter.Tk()
  window.title("palette")
  window.geometry('{}x{}'.format(XMAX, YMAX))
  window.bind("<Key>", keypress)
  return window

# Create canvas and add to main window
def create_canvas(window):
  canvas = tkinter.Canvas(window)
  canvas.configure(bg="black")
  canvas.pack(fill="both", expand=True)
  return canvas

def draw(window, canvas):
  for y in range (0,ROWS):
    for x in range (0,COLS):
      canvas.create_rectangle(x*WIDTH, y*HEIGHT, (x+1)*WIDTH, (y+1)*HEIGHT, fill=BOLOKAI[x+y*COLS])
      canvas.create_text(x*WIDTH+WIDTH/2, y*HEIGHT+HEIGHT/2, text=NAMES[x+y*COLS])

  while not done:
    window.update()

  window.destroy()

# Main
done = False
window = create_window()
canvas = create_canvas(window)
draw(window, canvas)
