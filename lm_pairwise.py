import tkinter
import math
import random

N = 8
GRID = 40
BLOB = GRID>>2
XMAX = 2*GRID+int(N*math.log2(N)*(math.log2(N)-1)/4+N-1)*GRID
YMAX = GRID+N*GRID

# Main window
def create_window():
    window = tkinter.Tk()
    window.title('Pairwise')
    window.geometry('{}x{}'.format(XMAX, YMAX))
    return window

# Create canvas and add to main window
def create_canvas(window):
    canvas = tkinter.Canvas(window)
    canvas.configure(bg=darkgray)
    canvas.pack(fill='both', expand=True)
    x = GRID>>1
    for y in range(0, N):
        canvas.create_line(0, GRID+GRID*y, XMAX, GRID+GRID*y, width=4, fill=pastelorange)
        canvas.create_oval(x-BLOB, GRID+GRID*y-BLOB, x+BLOB, GRID+GRID*y+BLOB, width=BLOB, outline=pastelorange, fill=pastelorange)
        canvas.create_oval(XMAX-2*BLOB, GRID+GRID*y-BLOB, XMAX, GRID+GRID*y+BLOB, width=BLOB, outline=pastelorange, fill=pastelorange)
    return canvas

def pairwise(window, canvas, data):
    x = GRID>>1
    for y in range(0, N):
        canvas.create_text(x, GRID+GRID*y, text=data[y])
    col = 0
    x = GRID + (GRID>>1)

    # Create the lexicographically sorted pair set
    a = 1
    while a < N:
        b = a
        c = 0
        while b < N:
            canvas.create_line(x, GRID+GRID*(b-a), x, GRID+GRID*b, width=BLOB, fill=COLOR[col])
            canvas.create_oval(x-BLOB, GRID+GRID*(b-a)-BLOB, x+BLOB, GRID+GRID*(b-a)+BLOB, width=BLOB, outline=COLOR[col], fill=COLOR[col])
            canvas.create_oval(x-BLOB, GRID+GRID*b-BLOB, x+BLOB, GRID+GRID*b+BLOB, width=BLOB, outline=COLOR[col], fill=COLOR[col])
            if data[b-a] > data[b]:
                data[b-a], data[b] = data[b], data[b-a]
                canvas.create_text(x, GRID+GRID*(b-a), text=data[b-a])
                canvas.create_text(x, GRID+GRID*b, text=data[b])
            x = x + GRID
            b = b + 1
            c = c + 1
            if c >= a:
                c = 0
                b = b + a
        a = a << 1
        col = col + 1

    # Begin the pairwise sort
    a = N >> 2
    e = 1
    while a > 0:
        d = e
        while d > 0:
            b = (d + 1) * a
            c = 0
            while b < N:
                canvas.create_line(x, GRID+GRID*(b-d*a), x, GRID+GRID*b, width=BLOB, fill=COLOR[col])
                canvas.create_oval(x-BLOB, GRID+GRID*(b-d*a)-BLOB, x+BLOB, GRID+GRID*(b-d*a)+BLOB, width=BLOB, outline=COLOR[col], fill=COLOR[col])
                canvas.create_oval(x-BLOB, GRID+GRID*b-BLOB, x+BLOB, GRID+GRID*b+BLOB, width=BLOB, outline=COLOR[col], fill=COLOR[col])
                if data[b-d*a] > data[b]:
                    data[b-d*a], data[b] = data[b], data[b-d*a]
                    canvas.create_text(x, GRID+GRID*(b-d*a), text=data[b-d*a])
                    canvas.create_text(x, GRID+GRID*b, text=data[b])
                x = x + GRID
                b = b + 1
                c = c + 1
                if c >= a:
                    c = 0
                    b = b + a
            d = d >> 1
        a = a >> 1
        col = col + 1
        e = 2*e + 1;
    for y in range(0, N):
        canvas.create_text(XMAX-BLOB, GRID+GRID*y, text=data[y])

    window.update()
    return data

# Main
with open('lm_bolokai.py') as f: exec(f.read())
COLOR = [pastelblue, pastelyellow, pastelpurple, pastelgreen, pastelpink,
        darkred, darkgreen, darkblue, brightgreen, darkmagenta, darkwhite, black]


window = create_window()
canvas = create_canvas(window)

data = list(range(0, N))
random.shuffle(data)
print(data)
data = pairwise(window, canvas, data)
print(data)
i=input('ENTER TO CLOSE')
window.destroy()
