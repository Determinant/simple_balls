"""
 vim: set ts=4 sw=4 fdm=marker 
 Copyright (C) 2011-2012 Ted Yin <ted.sybil@gmail.com>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 @author Ted Yin

"""

from math import sqrt

EPS = 1e-6

class Vect2D(object):

    '''
        The abstract of vectors

        (x, y) stands for a two-dimensional vector
    '''
    
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, b):
        """ Operator overload for plus sign"""
        return Vect2D(self.x + b.x, self.y + b.y)

    def __sub__(self, b):
        """ Operator overload for minus sign."""
        return Vect2D(self.x - b.x, self.y - b.y)

    def __mul__(self, b):
        """ Operator overload for time sign."""
        return Vect2D(self.x * float(b), self.y * float(b))

    def __div__(self, b):
        """ Operator overload for division sign."""
        return Vect2D(self.x / float(b), self.y / float(b))

    def det(self, b):
        """ Calculate cross product of two vectors."""
        return self.x * b.y - b.x * self.y

    def dot(self, b):
        """ Calculate inner product of two vectors."""
        return self.x * b.x + self.y * b.y

    def scale(self, b):
        """ Scale the vector by a pair of factors (denoted by b). """
        return Vect2D(self.x * b.x, self.y * b.y)

    def rev_scale(self, b):
        """ Reverse scale, see scale. """
        return Vect2D(self.x / b.x, self.y / b.y)

    def length(self):
        """ Get the length of the vector. """
        return sqrt(self.x ** 2 + self.y ** 2)

    def unit(self):
        """ Normalize the vector. """
        return self / self.length() 

    def print_(self):
        """ For debug use. """
        print self.x, self.y

    def round_(self):
        """ Round the values. """
        return Vect2D(round(self.x, 3),
                        round(self.y, 3))
    def get_str(self):
        """ Convert the vector into a string. """
        return "(" + str(round(self.x, 2)) + ", " + str(round(self.y, 2)) + ")"

class PhysicalSprite(object):

    '''
        The physical abstract of objects

        shift -- Shift          Vect2D
        velo -- Velocity        Vect2D
        accel -- Acceleration   Vect2D
        mass -- Mass            float
    '''

    sprite_list = []

    def __init__(self, shift, velo, accel, mass):
        self.shift = shift
        self.velo = velo
        self.accel = accel
        self.mass = mass
        PhysicalSprite.sprite_list.append(self)

    def solve_collision(self):
        """ Meta function for solving collision. """
        for obj in PhysicalSprite.sprite_list:
            self._solve_collision(obj)


    def move(self, dt):
        """ Calculate the current status according to Newton's Second Law. """
        self.shift += self.velo * dt + self.accel * 0.5 * (dt ** 2)
        self.velo += self.accel * dt
        self.solve_collision()

