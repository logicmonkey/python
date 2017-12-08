#!/usr/bin/env python

################################################################################
#                                                                              #
#                             lm_wxgraphic.py                                  #
#                                                                              #
################################################################################
#                                                                              #
#  Generates a graphic for time, temperature, the day's rainfall and           #
#  recent wind statistics from the WOSPi XML file /var/tmp/wxdata.xml          #
#                                                                              #
#  It's almost fully self-contained, no base bitmaps are used but two fonts    #
#  are pulled in. To get this working on a Raspberry Pi You will need to get   #
#  as root:                                                                    #
#                                                                              #
#   # apt-get install python-cairo                                             #
#   # apt-get install python-setuptools && easy_install pip                    #
#   # pip install xmltodict                                                    #
#                                                                              #
#  Cairo is your vector drawing stuff, xmltodict reads the XML into dictionary #
#                                                                              #
#  The 7-ish segment LED font (Lets-go-Digital) can be installed with:         #
#                                                                              #
#   # wget http://www.ffonts.net/Lets-go-Digital-Regular.font.zip              #
#   # mkdir letsgodigital                                                      #
#   # cd letsgodigital                                                         #
#   # unzip ../Lets-go-Digital-Regular.font.zip                                #
#   # mkdir /usr/share/fonts/letsgodigital                                     #
#   # cp Let\'s\ go\ Digital\ Regular.ttf /usr/share/fonts/letsgodigital       #
#   # fc-cache                                                                 #
#                                                                              #
#  Re-use this code as you wish, but please acknowledge where it came from     #
#                                                                              #
#                                                              -=LogicMonkey=- #
#                                                                              #
################################################################################

import datetime                    # for adding the time to the text fields
import math                        # for 3.141592653
import cairo                       # for drawing
#import xmltodict                   # https://github.com/martinblech/xmltodict

def lm_wxgraphic (width, height, png_output):

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#                                                                              #
#                             lm_anemometer                                    #
#                                                                              #
#                            gust : red needle                                 #
#                   current speed : green needle                               #
#                2 minute average : pale blue needle                           #
#               10 minute average : paler blue needle                          #
#                                                                              #
#  A 270 degree arc is sub-divided into a 0-100 scale and then numbered.       #
#  Indicator needles are then applied                                          #
#                                                                              #
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    def lm_anemometer (spd_now, spd_2, spd_10, spd_gust, spd_unit):

        ''' there are 4 indicators
        '''
        def lm_clamp (f):
            if f > 100.0:
                return 100.0
            elif f < 0.0:
                return 0.0
            return f

        speed_now  = lm_clamp (float (spd_now))
        speed_2    = lm_clamp (float (spd_2))
        speed_10   = lm_clamp (float (spd_10))
        speed_gust = lm_clamp (float (spd_gust))
        speed_unit = spd_unit

        mindim = min(width, height)/2.0   # a reference measurement on which to base other sizes
                                          #   e.g. the font size and line widths

        radius = mindim * 0.9  # don't extend all the way to the edge

        ''' draw dial with markers at 5s and 10s
        '''
        # have the 0-100 dial run from 135 to 135+270=45
        def lm_num_to_angle (num):
           return ((num/100.0 * 270) + 135.0) * (math.pi/180.0) # deg to rad 2pi/360

        # draw_radius starts at some point on a circle and draws a radius to the centre
        # num is a percentage (or a value with range 0-100!)
        def lm_draw_radius (radius, num):
            phi = lm_num_to_angle (num)
            cr.arc (0, 0, radius, phi, phi)
            cr.line_to (0, 0)
            cr.stroke ()

        # draw filled circle
        cr.set_source_rgba (1, 1, 1, 1)       # white
        cr.arc (0, 0, radius, 0, 2*math.pi)
        cr.fill ()

        # draw border
        cr.set_line_width (mindim/40.0)
        cr.set_source_rgba (0, 0, 0, 1)       # black
        cr.arc (0, 0, radius, 0, 2*math.pi)
        cr.stroke ()

        #draw draw_radii at modulo 10 + 5

        for i in range (0, 10):
            lm_draw_radius (radius, i*10+5)

        # draw filled circle clipping the 5-markers
        cr.set_source_rgba (1, 1, 1, 1)       # white
        cr.arc (0, 0, radius*0.95, 0, 2*math.pi)
        cr.fill ()

        #draw draw_radii at modulo 10
        cr.set_source_rgba (0, 0, 0, 1)       # black

        for i in range (0, 11):
            lm_draw_radius (radius, i*10)

        # draw filled circle cliiping the 10-markers
        cr.set_source_rgba (1, 1, 1, 1)       # white
        cr.arc (0, 0, radius*0.90, 0, 2*math.pi)
        cr.fill ()

        # apply numbers to 10-markers
        cr.set_source_rgba (0, 0, 0, 1)       # black
        cr.select_font_face ("DejaVu Sans Mono", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size (mindim/10)

        for num in range(0, 11):
            phi = lm_num_to_angle (num*10)
            cr.arc (0, 0, 0.75*radius, phi, phi)
            cr.rel_move_to (-mindim/24, mindim/24)       # nudge down and left
            cr.show_text(("%d") % (num*10))
            cr.stroke ()

        ''' indicator key text
        '''
        cr.set_source_rgba (0, 0, 0, 1)          # black
        string = "WIND(%s)" % speed_unit
        bb = cr.text_extents (string)
        ystride = bb[3]                          #extents: [2] is width, [3] is height
        cr.move_to (-bb[2]/2, 3*bb[3])
        cr.show_text (string)
        cr.stroke ()

        cr.set_source_rgba (0.8, 0.2, 0.2, 1.0)  # red
        string = "GUST"
        bb = cr.text_extents (string)
        cr.move_to (-bb[2]/2, 4*ystride)
        cr.show_text (string)
        cr.stroke ()

        cr.set_source_rgba (0.2, 0.8, 0.2, 1.0)  # green
        string = "CURRENT"
        bb = cr.text_extents (string)
        cr.move_to (-bb[2]/2, 5*ystride)
        cr.show_text (string)
        cr.stroke ()

        cr.set_source_rgba (0.2, 0.2, 1.0, 0.5)  # blue
        string = "2'average"
        bb = cr.text_extents (string)
        cr.move_to (-bb[2]/2, 6*ystride)
        cr.show_text (string)
        cr.stroke ()

        cr.set_source_rgba (0.2, 0.2, 1.0, 0.3)  # pale blue
        string = "10'average"
        bb = cr.text_extents (string)
        cr.move_to (-bb[2]/2, 7*ystride)
        cr.show_text (string)
        cr.stroke ()


        ''' finally draw indicators - they get skinnier as we go
        '''
        cr.move_to(0, 0)

        cr.set_line_width (mindim/40.0)
        cr.set_line_cap (cairo.LINE_CAP_ROUND)
        cr.stroke ()

        cr.set_line_width (mindim/44.0)
        cr.set_source_rgba (0.2, 0.2, 1.0, 0.5)  # blue
        lm_draw_radius (radius*0.9, speed_2)

        cr.set_line_width (mindim/48.0)
        cr.set_source_rgba (0.2, 0.2, 1.0, 0.3)  # pale blue
        lm_draw_radius (radius*0.9, speed_10)

        # draw the opaque after the non-opaque
        cr.set_line_width (mindim/52.0)
        cr.set_source_rgba (0.8, 0.2, 0.2, 1.0)  # red
        lm_draw_radius (radius*0.9, speed_gust)

        cr.set_line_width (mindim/56.0)
        cr.set_source_rgba (0.2, 0.8, 0.2, 1.0)  # green
        lm_draw_radius (radius*0.9, speed_now)

        # centre dot
        cr.set_source_rgba (0, 0, 0, 1)          # black
        cr.arc (0, 0, mindim/15.0, 0, 2*math.pi)
        cr.fill ()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#                                                                              #
#    simple 4x 20% height fields spaced vertically with 4% margin              #
#                                                                              #
#                  +-------------+--------------+                              #
#            4     |                   o  o     |                              #
#            20+4  | TIME           o        o  |                              #
#            20+4  | TEMP          o          o |                              #
#            20+4  | RAIN          o          o |                              #
#            20    | WIND           o        o  |                              #
#            4     |                   ----     |                              #
#                  +-------------+--------------+                              #
#                                                                              #
#    0xFF2a2a is a nice LED red for the text                                   #
#                                                                              #
#    60 point "Let's Go Digital" LED font fits at 200 height                   #
#                                                                              #
#    layout should also work at 90 degrees with minimal hacking (*)            #
#                                                                              #
#                        +--------------+                                      #
#                        |     o  o     |                                      #
#                        |  o        o  |                                      #
#                        | o          o |                                      #
#                        | o          o |                                      #
#                        |  o        o  |                                      #
#                        |     ----     |                                      #
#                        |_            _|                                      #
#                        |              |                                      #
#                        | TIME         |                                      #
#                        | TEMP         |                                      #
#                        | RAIN         |                                      #
#                        | WIND         |                                      #
#                        |              |                                      #
#                        +--------------+                                      #
#                                                                              #
#    (*) - it does work, but landscape still looks nicer on iPhone             #
#                                                                              #
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context (surface)

    def lm_textfield (string, field_id):

        cr.select_font_face ("Let's Go Digital", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size (60 * min(height, width)/200)
        cr.set_source_rgba (1.0, 0.16, 0.16, 1.0)  # LED colour ff2a2aff

        bb = cr.text_extents (string)  # (bearing_x, bearing_y, width, height, adv_x, adv_y)
        posx = min(height, width)*0.04
        posy = (bb[3] + min(height, width)*0.04) * field_id # bb[3] is text height

        cr.move_to (posx, posy)
        cr.show_text (string)
        cr.stroke ()
        return (posx + bb[4], posy) # save current pen position if adding units in another font

    def lm_textfield_unit (string, posxy):

        cr.select_font_face ("DejaVu Sans Mono", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size (30 * min(height, width)/200)
        cr.set_source_rgba (0.8, 0.16, 0.16, 1.0)  # slightly darker than LEDs

        cr.move_to (posxy[0], posxy[1])
        cr.show_text (string)
        cr.stroke ()
        return

    def lm_dirn (degs):
        comp = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        return comp [int(16*degs/360.0)]

    #
    # TEXT
    #
    # origin translations for different aspects

    if width > height:          # landscape
        xo = width - 2*height   #     +---------------o---+---+
        yo = 0                  #     |               |   |   |
                                #     +---------------+---+---+
    else:
        xo = 0                  # don't do anything if portrait
        yo = 0

    cr.translate (xo, yo)


    lm_textfield (("%s" % datetime.datetime.now().strftime("%H:%M")), 1)

    # show units in a different font because a) they won't fit and b) they're constant
    # use the advance_x at the current y to place the unit text
    posxy = lm_textfield (("%+.1f" % temp_now), 2)
    lm_textfield_unit (u' \u00B0C', posxy)

    posxy = lm_textfield (("%.1f" % rain_today), 3)
    lm_textfield_unit (" mm", posxy)

    posxy = lm_textfield (("%s %d" % (lm_dirn(wind_degrees), wind_spd_now)), 4)
    lm_textfield_unit (" mph", posxy)

    cr.translate (-xo, -yo)

    #
    # DIAL
    #
    if width > height:          # landscape
        xo = width - height/2.0 #     +---------------+---+---+
        yo = height/2.0         #     |               |   | o |
                                #     +---------------+---+---+
    else:
        xo = width/2.0          # portrait is centre, centre bottom half
        yo = height - width/2.0

    cr.translate (xo, yo)
    lm_anemometer (wind_spd_now, wind_spd_2, wind_spd_10, wind_spd_gust, 'mph')
    cr.translate (-xo, -yo)

    surface.write_to_png (png_output)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#                                                                              #
#                                     MAIN                                     #
#                                                                              #
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

"""
with open ("/var/tmp/wxdata.xml", "r") as wxfile:
    wxdata_string = wxfile.read ()

wxdata = xmltodict.parse (wxdata_string)

wind_spd_now  = float (wxdata['wxdata']['wind_mph'])
wind_spd_2    = float (wxdata['wxdata']['avgwind2_mph'])
wind_spd_10   = float (wxdata['wxdata']['avgwind10_mph'])
wind_spd_gust = float (wxdata['wxdata']['gust10_mph'])
wind_degrees  = float (wxdata['wxdata']['winddir'])
rain_today    = float (wxdata['wxdata']['dayrain_mm'])
temp_now      = float (wxdata['wxdata']['outtemp_c'])
"""

wind_spd_now  = 28
wind_spd_2    = 26
wind_spd_10   = 30
wind_spd_gust = 45
wind_degrees  = 239
rain_today    = 7.7
temp_now      = 18.1

lm_wxgraphic (1000, 288, 'lm_wospiwx.png')          # Wordpress dimensions
lm_wxgraphic ( 960, 480, 'lm_wospiwx_iphone.png')   # iPhone4 resolution
