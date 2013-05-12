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

import simulate
from graphics import PhyUI
from physics import Vect2D
from Tkinter import Tk

def main():

    root = Tk()
    app = PhyUI(root, 1000, 500)
    app.set_viewport(Vect2D(0, 0), Vect2D(200, 100))
  
    all_ = []

     
    # Four boundaries

    all_.append(simulate.Ball(
            radius = 20, shift = Vect2D(5 * 10 + 10, 2 * 10 + 10), 
            velo = Vect2D(0, 0), accel = Vect2D(0, 0), 
            mass = 5, app = app))
 
    all_.append(simulate.Ball(
            radius = 20, shift = Vect2D(0 * 10 + 10, 5 * 10 + 10), 
            velo = Vect2D(5, 0), accel = Vect2D(0, 0), 
            mass = 5, app = app))
 


    # Some balls for testing

    for i in all_:
        app.register_trigger(i, 5, 0.007)

    # Register in display callback

    root.mainloop()

main()
