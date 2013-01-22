from math import fabs
from time import sleep
from copy import deepcopy
from itertools import permutations
from decimal import Decimal
from gravsim.vec2d import vec2d

class Simulation (object):
    """
    This class represents the running simulation
    works on objects which have collide, move, accelerate methods
    and position and velocity parameters
    """

    def __init__(self, things, borders, stepsize = .1):
        """
        Constructor.
        
        gravwell -- two-tuple, position and mass of gravity well
        things -- objects to simulate
        borders -- tuple of vec2d describing where balls should bounce
        stepsize -- time in seconds which shall be simulated in one step
        """

        self.things   = things
        self.walls    = borders
        self.stepsize = stepsize
        self.gconst   = Decimal ('6.67384e-11') * 10000000000
        self.time     = 0

    def grav_accel (self, mass1, mass2, radius):
        """
        return the accelerations on mass2
        """

        return (self.gconst * mass1 * mass2 / radius ** 2) / mass2

    def get_grav_force (self, mass1, mass2, radius):

        return (self.gconst * mass1 * mass2 / radius ** 2)

    def step (self):

        for thing in self.things:
            self.time += self.stepsize
            thing.move (self.stepsize)
            trad = thing.radius

            for premise, border in self.walls:

                radius_vector = trad * border.perpendicular_normal ()
                
                present_angle = border.get_angle_between (thing.position - premise + radius_vector)
                future_angle = border.get_angle_between (
                        thing.position + thing.velocity * self.stepsize / 2 - premise - radius_vector
                )
                sign_p = present_angle / Decimal (fabs (present_angle)) if present_angle != 0 else 1
                sign_f = future_angle / Decimal (fabs (future_angle)) if future_angle != 0 else -1 * sign_p
                if sign_p != sign_f or present_angle == 0:
                    if not premise.length < thing.position.length < (premise + border).length:
                        continue
                    v_angle = border.get_angle_between (thing.velocity)
                    thing.velocity.rotate (-1 * 2 * v_angle)

        for thing, other in permutations (self.things, 2):

            grav_dir = (other.position - thing.position)
            grav_dir_norm = grav_dir.normalized ()
            grav_force = grav_dir * self.get_grav_force (
                    other.mass, thing.mass, grav_dir.length)
            thing.accelerate (id (other), grav_force/thing.mass)
            other.accelerate (id (thing), -grav_force/other.mass)

            future_thing = deepcopy (thing)
            future_other = deepcopy (other)
            future_thing.move (self.stepsize)
            future_other.move (self.stepsize)
            vec_dist = abs (future_other.position - future_thing.position)
            if vec_dist.length - thing.radius - other.radius <= 0: # things collide
                horizontal = vec_dist.perpendicular_normal ()
                thing.velocity.rotate (-1 * 2 * horizontal.get_angle_between (thing.velocity))
                other.velocity.rotate (-1 * 2 * horizontal.get_angle_between (other.velocity))
