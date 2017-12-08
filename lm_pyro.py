#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import string
import random

W = 360
H = 120

RCOEFF = 23 # a residual multiplier for the sample point
HCOEFF = 45 # diffusion coefficients
VCOEFF = 69 # make these 8 bit and then /256 at point of use

def clamp(n):
    if n < 0:
        return 0
    if n > 255:
        return 255
    return int(n)

def draw_rgb_image(area, event):

    for x in range (W):
        bitmap[(H-1)*W + x] = random.randint(0,255)

    for y in range (2, H): # top margin at 2 so y-2 won't underflow

        # move down image smear the centre bottom sample upwards and outwards
        #
        #     _       y increases down the screen y=0 to H-1
        #   _|_|_     x, y-2
        #  |_+_+_|    x-1 to x+1, y-1
        #  |_+_+_|    x-1 to x+1, y
        #
        for x in range (1, W-1): # L and R margin so x won't under/overflow

            hdelta = (bitmap[y*W+x] * HCOEFF)>>8
            vdelta = (bitmap[y*W+x] * VCOEFF)>>8

            # central column of 3 samples
            bitmap[(y-2)*W + x] += (vdelta>>1)
            bitmap[(y-1)*W + x] +=  vdelta
            bitmap[  y  *W + x] = (bitmap[y*W+x] * RCOEFF)>>8

            # middle two outer samples
            bitmap[(y-1)*W + x-1] += hdelta
            bitmap[(y-1)*W + x+1] += hdelta

            # bottom two outer samples (half delta)
            bitmap[y*W + x-1] += (hdelta>>1)
            bitmap[y*W + x+1] += (hdelta>>1)

    for p in range (W*H):
        rgb[3*p]   = chr(clamp(bitmap[p]))  # R
#       rgb[3*p+1] = chr(clamp(0.2*bitmap[p]))  # G
#       rgb[3*p+2] = chr(clamp(bitmap[p]))  # B

    buff = string.join(rgb, '')

    style = area.get_style()
    gc = style.fg_gc[gtk.STATE_NORMAL]

    area.window.draw_rgb_image(gc, 0, 0, W, H,
              gtk.gdk.RGB_DITHER_NONE, buff, W*3)
    area.queue_draw() # schedule re-draw straight away
    return True

###############################################################
#                              MAIN                           #
###############################################################
window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.connect("destroy", lambda w: gtk.main_quit())

area = gtk.DrawingArea()
area.set_size_request(W, H)

table = gtk.Table(1,1)
table.attach(area, 1, 2, 1, 2)
window.add(table)

bitmap = [0]*W*H
rgb=['\0']*3*W*H

area.connect("expose-event", draw_rgb_image)
area.show()
table.show()
window.show()

gtk.main()

