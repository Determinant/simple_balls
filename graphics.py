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

from physics import Vect2D
from Tkinter import Canvas, Frame, Button, Label, LabelFrame, Entry

class PhyUI():

    def callback_switcher(self):
        """ Callback function for switching status between 
            'freezed' and 'on going'. """

        play_ref = self.button_play
        if not self.locked :
            play_ref.config(text = "Play")
            self.locked = True
        else:
            play_ref.config(text = "Freeze")
            self.locked = False

    def keyevent_up_press(self, event):
        """ Callback for pressing up key. """
        self.mouse_lock = True
        self.selected_user_accel_factor[0] = 1

    def keyevent_up_release(self, event):
        """ Callback for releasing up key. """
        self.mouse_lock = False
        self.selected_user_accel_factor[0] = 0

    def keyevent_down_press(self, event):
        """ Callback for pressing down key. """
        self.mouse_lock = True
        self.selected_user_accel_factor[1] = 1

    def keyevent_down_release(self, event):
        """ Callback for releasing down key. """
        self.mouse_lock = False
        self.selected_user_accel_factor[1] = 0

    def keyevent_left_press(self, event):
        """ Callback for pressing left key. """
        self.mouse_lock = True
        self.selected_user_accel_factor[2] = 1

    def keyevent_left_release(self, event):
        """ Callback for releasing left key. """
        self.mouse_lock = False
        self.selected_user_accel_factor[2] = 0

    def keyevent_right_press(self, event):
        """ Callback for pressing right key """
        self.mouse_lock = True
        self.selected_user_accel_factor[3] = 1

    def keyevent_right_release(self, event):
        """ Callback for releasing right key """
        self.mouse_lock = False
        self.selected_user_accel_factor[3] = 0

    def __init__(self, root_handle, canvas_width, canvas_height):
        """ Setup the whole application."""

        self.locked = True  # True for freeze.
        self.mouse_lock = False # True for locking the mouse behavior.
        self.selected = None # What ball is selected now?
        self.selected_user_accel_factor = [0, 0, 0, 0] # Acceleration from user's keypress event
        self.selected_user_accel_val = [Vect2D(0, 15), 
                                        Vect2D(0, -5),
                                        Vect2D(-5, 0), 
                                        Vect2D(5, 0)] 

        self.circles = [] # Reference to all the balls.

        # Initialize the main variables for the application

        self.frm_main = Frame(root_handle)
        self.frm_side_top = LabelFrame(root_handle, 
                                        text = "Realtime Parameters:")
        self.frm_side_bot = Frame(root_handle)

        # Setup the frames

        self.canv_width = canvas_width
        self.canv_height = canvas_height
        self.canvas_base = Vect2D(0, self.canv_height)
        self.canvas = Canvas(
                self.frm_main, 
                width = self.canv_width, height = self.canv_height, 
                bg = "#cccccc")
        # Setup the canvas

        self.canvas.bind_all("<KeyPress-w>", self.keyevent_up_press)
        self.canvas.bind_all("<KeyRelease-w>", self.keyevent_up_release)
        self.canvas.bind_all("<KeyPress-a>", self.keyevent_left_press)
        self.canvas.bind_all("<KeyRelease-a>", self.keyevent_left_release)
        self.canvas.bind_all("<KeyPress-d>", self.keyevent_right_press)
        self.canvas.bind_all("<KeyRelease-d>", self.keyevent_right_release)
        self.canvas.bind_all("<KeyPress-s>", self.keyevent_down_press)
        self.canvas.bind_all("<KeyRelease-s>", self.keyevent_down_release)

        # Setup all keys
 
        self.button_play = Button(self.frm_side_bot, 
                                    text = "Play", 
                                    command = self.callback_switcher)
        self.button_add = Button(self.frm_side_bot, 
                                    text = "Exit", 
                                    command = root_handle.quit)

        # Setup all the buttons

        side_names = ["Mass", "Positioin", "Velocity", "Acceleration"]
        self.side_label = []
        self.side_entry = []
        for name in side_names:
            self.side_label.append(Label(self.frm_side_top, text = name + ":"))
            self.side_entry.append(Label(self.frm_side_top, width = 20))

        # Setup information area located on the sidebar

        self.frm_main.grid(row = 0, column = 0, rowspan = 2)
        self.frm_side_top.grid(row = 0, column = 1, sticky = "S")
        self.frm_side_bot.grid(row = 1, column = 1, sticky = "S")
        self.canvas.grid(row = 0, column = 0, columnspan = 2)
        self.button_play.grid(row = 1, column = 0, sticky = "E")
        self.button_add.grid(row = 1, column = 1, sticky = "W")
        for i in xrange(len(self.side_label)):
            self.side_label[i].grid(row = i, column = 0)
            self.side_entry[i].grid(row = i, column = 1)

        # Build up the layout

    def set_viewport(self, math_bl, math_tr):
        """ 
            Set the translation rate.
            You should call this before calling trans or rev_trans.
        """

        self.scale_factor = Vect2D(
                self.canv_width / float(math_tr.x - math_bl.x),
                -self.canv_height / float(math_tr.y - math_bl.y))

        self.math_base = math_bl

    def trans(self, pos):
        """ Translation (from math coord to canvas coord)."""

        return (pos - self.math_base).scale(self.scale_factor) + \
            self.canvas_base

    def rev_trans(self, pos):
        """ Reverse translation (from canvas coord to math coord)."""

        return (pos - self.canvas_base).rev_scale(self.scale_factor) + \
            self.math_base

    def canvas_refresh(self, id, vertexes):
        """ Refresh the canvas """
        self.canvas.coords(id, vertexes)

    def update_side_bot(self):
        """ Update the information posted on the side bar."""
        if self.selected: 
            self.side_entry[0].config(text = str(self.selected.mass))
            self.side_entry[1].config(text = self.selected.shift.get_str())
            self.side_entry[2].config(text = self.selected.velo.get_str())
            self.side_entry[3].config(text = self.selected.accel.get_str())
        else:
            for i in xrange(4):
                self.side_entry[i].config(text = "")


    def create_circle(self, vertexes):
        """ Create a circle graphically and return the id of the object. """

        return self.canvas.create_oval(
                vertexes,
                fill="white"
                )

    def create_line(self, vertexes):
        """ Create a line graphically and return the id of the object."""
        return self.canvas.create_line(vertexes)

    def register_trigger(self, obj, real_interval, math_interval):
        """ Call this for hooking any simulated objects."""
        self.canvas.after(
                real_interval, obj.refresh, real_interval, math_interval)
        
