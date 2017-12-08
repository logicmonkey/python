#!/usr/bin/env python

import pygtk
import gtk, gobject, cairo
from gtk import gdk

import math

class Screen( gtk.DrawingArea ):
    def __init__( self, width, height ):
        super( Screen, self ).__init__()
        self.connect( "expose_event", self.do_expose_event )
        self.connect( "button_press_event", self.do_button_press_event )
        self.add_events( gdk.BUTTON_PRESS_MASK | gdk.BUTTON_RELEASE_MASK )
        # animate
        gobject.timeout_add( 10, self.invalidate ) # call every 10
        self.set_size_request( width, height )
        self.width  = width
        self.height = height
        self.pause = False

    def invalidate( self ):
        if self.pause == False:
            # unless paused, invalidate screen causing the expose event
            self.alloc = self.get_allocation( )
            rect = gtk.gdk.Rectangle( 0, 0, self.alloc.width, self.alloc.height )
            self.window.invalidate_rect( rect, True )
        return True # allow timeout to tick again

    def do_expose_event( self, widget, event ):
        self.cr = self.window.cairo_create()
        self.draw()

    def do_button_press_event( self, widget, event ):
        self.pause = not self.pause

class phasor( Screen ):
    def __init__( self, width, height ):
        Screen.__init__( self, width, height )
        self.deg = 0.0
        self.dir = 1

    def draw( self ):
        cr = self.cr # context shortcut
        pi = math.pi
        cr.set_line_width( 1.0 )
        scale = 0.9  # choose not to draw to window edge

        # sine wave
        cr.set_source_rgb( 1, 0, 0 )
        for xpos in range(360):
      	    cr.move_to( self.height + xpos, self.height/2 )
      	    cr.line_to( self.height + xpos,
                        self.height/2 * (1.0 - scale * math.sin(xpos * pi / 180.0)))
        cr.stroke()

        # circle
        cr.set_source_rgb( 0, 1, 0 )
        cr.arc( self.height/2, self.height/2, scale*self.height/2, 0, 2 * pi)
        cr.stroke()

      	# phasor
        cr.set_source_rgb( 0, 0, 1 )
        cr.move_to( self.height/2, self.height/2 ) # centre
        cr.line_to( self.height/2 * (1.0 - scale * math.cos(pi + self.deg * pi / 180.0)),
                    self.height/2 * (1.0 - scale * math.sin(     self.deg * pi / 180.0)) )

        # cursor on sine wave
        cr.line_to( self.height + self.deg,
                    self.height/2 * (1.0 - scale * math.sin(self.deg * pi / 180.0)) )
        cr.line_to( self.height + self.deg, self.height/2 )
        cr.stroke()

        self.deg += self.dir

        if self.deg == 0 or self.deg == 360:
            self.dir *= -1

def run( Widget, width, height ):
    window = gtk.Window()
    window.connect( "delete-event", gtk.main_quit )
    widget = Widget( width, height )
    widget.show()
    window.add( widget )
    window.present()
    gtk.main()

run( phasor, 300+360+10, 300 )
