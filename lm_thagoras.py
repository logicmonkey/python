#!/usr/bin/python

################################################################################
#
#                           Pythagoras's Theorem
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

import pygtk
import gtk, gobject, cairo
from gtk import gdk

class Screen( gtk.DrawingArea ):
    def __init__( self, height ):
        super( Screen, self ).__init__()
        self.connect( "expose_event", self.do_expose_event )
        self.connect( "button_press_event", self.do_button_press_event )
        self.add_events( gdk.BUTTON_PRESS_MASK | gdk.BUTTON_RELEASE_MASK )
        # animate
        gobject.timeout_add( 10, self.invalidate ) # call every 10
        self.set_size_request( height, height )
        self.height = height
        self.pause = False

    def invalidate( self ):
        if self.pause == False:
            # unless paused, invalidate screen causing the expose event
            self.alloc = self.get_allocation( )
            rect = gtk.gdk.Rectangle( self.alloc.x, self.alloc.y,
                                      self.alloc.width, self.alloc.height )
            self.window.invalidate_rect( rect, True )        
        return True # allow timeout to tick again

    def do_expose_event( self, widget, event ):
        self.cr = self.window.cairo_create()
        self.draw()

    def do_button_press_event( self, widget, event ):
        self.pause = not self.pause

class Pythagoras( Screen ):
    def __init__( self, height ):
        Screen.__init__( self, height )
        self.a = 0
        self.direction = 1 # +1 or -1 signed increment for a

    def draw( self ):
        cr = self.cr # context shortcut
        cr.set_line_width( 1.0 )
        
        b = self.height-1-self.a
        
        cr.set_source_rgb( 0, 1, 0 )
        cr.rectangle( 0, 0, self.a, self.a ) # green a-squared
        cr.fill()
        
        cr.set_source_rgb( 1, 0, 0 )
        cr.rectangle( self.a, 0, b, b )      # red b-squared
        cr.fill()
        
        cr.set_source_rgb( 0, 0, 1 )
        cr.move_to( self.a+b, b )
        cr.line_to( b, 0 )                   # top lines of blue c-squared
        cr.line_to( 0, self.a )
        cr.stroke()
    
        cr.move_to( 0, self.a )              # blue triangle bottom left
        cr.line_to( 0, self.height-1 )       # draw only the perpendicular sides
        cr.line_to( self.a, self.height-1 )  # cairo will join the last two
        cr.fill()                            # points creating the hypotenuse
    
        cr.move_to( self.a, self.height-1 )  # bottom right line of blue square
        cr.line_to( self.height-1, b )
        cr.stroke()
    
        cr.set_source_rgb( 0, 0, 0 )
        cr.move_to( self.a, 0 )
        cr.line_to( self.a, self.a+b )       # black vertical
        cr.stroke()
    
        self.a += self.direction
    
        if self.a == self.height or self.a == 0: self.direction *= -1 # reverse

def run( Widget, height ):
    window = gtk.Window()
    window.connect( "delete-event", gtk.main_quit )
    widget = Widget( height )
    widget.show()
    window.add( widget )
    window.present()
    gtk.main()

run( Pythagoras, 700 )
