import pygame, sys
from pygame.locals import *
from math import ceil, sqrt
from time import sleep
from decimal import Decimal

from gravsim.vec2d import vec2d
from gravsim.things import Ball
from gravsim.simulation import Simulation

HEIGHT = Decimal (700)
WIDTH  = Decimal (700)
RAD    = Decimal ( 10)

WHITE  = Color (255, 255, 255)
BLACK  = Color (000, 000, 000)

CLOCK = pygame.time.Clock ()
DISPLAY = pygame.display.set_mode ((WIDTH, HEIGHT), RESIZABLE)

DISPLAY_BORDER = 50 
MAX_DISPLAY_LENGTH = Decimal (min (WIDTH, HEIGHT)) / 2 - DISPLAY_BORDER
balls  = (Ball (RAD, 100, (-50, 0), (40, 0)), Ball (RAD, 1, (20, 19), (-40, 0)))#, Ball (RAD, 10, (50, 300), (0, -15)))
earth = Ball (6371000, 10e24, (0, 0), (0, 0))
moon  = Ball (1737100, 10e21, (0, 20000000), (20220000, 0))
astro = Ball (RAD, 1000, (0, 100000), (2000000, 0))
solar = (earth, astro,)# moon)
things = balls
sim = Simulation (things, .01)

factor = Decimal ("1")

while True:

    DISPLAY.fill (WHITE)

    grav_center = \
        sum (t.mass * t.position for t in sim.things) / sum (t.mass for t in sim.things)
    max_position = 0
    #display_center = (WIDTH / 2, HEIGHT / 2) - grav_center

    pygame.draw.line (DISPLAY, BLACK, (0, grav_center [1]), 
            (WIDTH, grav_center [1]))
    pygame.draw.line (DISPLAY, BLACK, (grav_center [0], 0), 
            (grav_center [0], HEIGHT))

    for event in pygame.event.get ():
        if event.type == QUIT:
            pygame.quit ()
            sys.quit ()

        elif event.type == VIDEORESIZE:
            WIDTH, HEIGHT = Decimal (event.size [0]), Decimal (event.size [1])
            DISPLAY = pygame.display.set_mode ((WIDTH, HEIGHT), RESIZABLE)
            MAX_DISPLAY_LENGTH = Decimal (min (WIDTH, HEIGHT)) / 2

    for t in sim.things:
        print (t.position)
        if t.position.length > max_position:
            max_position = t.position.length

        display_pos = t.position - grav_center
        pygame.draw.circle (DISPLAY, BLACK, 
                (display_pos [0] * factor + WIDTH / 2,
                 display_pos [1] * factor + HEIGHT / 2),
                t.radius * factor)

    #factor = MAX_DISPLAY_LENGTH / max_position
    sim.step ()

    pygame.display.update ()
    CLOCK.tick (60)

