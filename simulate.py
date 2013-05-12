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

from physics import PhysicalSprite, EPS, Vect2D

class CanvasSprite():

    """ Canvas-level abstract (interact with the app). """
    def __init__(self, app):
        self.app = app
        self.canvas_refresh = app.canvas_refresh

    def refresh(self, rdt, dt):
        """ Refreshing callback for the canvas."""

        t = self.accel
        if self == self.app.selected:
            ta = self.app.selected_user_accel_factor
            tb = self.app.selected_user_accel_val
            for i in xrange(4):
                if (ta[i]): self.accel += tb[i]
            self.app.update_side_bot()

        if not self.app.locked: self.move(dt)
        self.canvas_refresh(self.id, self.get_vertexes())
        self.accel = t
        self.app.register_trigger(self, rdt, dt)

    def create_circle(self):
        self.id = self.app.create_circle(self.get_vertexes())
        self.app.circles.append(self)

    def create_line(self):
        self.id = self.app.create_line(self.get_vertexes())

class Ball(CanvasSprite, PhysicalSprite):

    def __init__(self, shift, velo, accel, mass, radius, app):
        PhysicalSprite.__init__(self, shift, velo, accel, mass)
        CanvasSprite.__init__(self, app)

        self.radius = radius
        self.create_circle()

        def selected(event):    # a closure for status changing
            if self.app.mouse_lock: return
            for i in self.app.circles:
                self.app.canvas.itemconfigure(i.id, fill = "white")
            self.app.canvas.itemconfigure(self.id, fill = "#0000ff")
            self.app.selected = self

        self.app.canvas.tag_bind(self.id, "<Button-1>", selected)

    def _solve_collision(self, obj):
        """ Solve the collision with another ball. """ 
        if obj.__class__ != Ball: return
        so = obj.shift - self.shift
        if abs(so.length()) < EPS: return
        so_u = so.unit()
        os_u = Vect2D(0, 0) - so_u
        vs = so_u.dot(self.velo)
        vo = os_u.dot(obj.velo)

        dis = self.radius + obj.radius - so.length()

        if dis > 0 and vs + vo > 0 :
            vo = -vo
            vs1 = ((self.mass - obj.mass) * vs + 2 * obj.mass * vo) /  \
                        (self.mass + obj.mass)
            vo1 = ((obj.mass - self.mass) * vo + 2 * self.mass * vs) / \
                        (self.mass + obj.mass)

            vo1 = -vo1 
            vo = -vo
            self.velo += so_u * (vs1 - vs)
            obj.velo += os_u * (vo1 - vo)

            ###################
            obj.shift += so_u * dis
            #obj.canvas_refresh(obj.id, obj.get_vertexes())
            #obj.solve_collision()
            ###### fix ########

    def get_vertexes(self):
        """ Get current position of the ball. """
        pos0 = self.app.trans(Vect2D(
            self.shift.x - self.radius, self.shift.y - self.radius))
        pos1 = self.app.trans(Vect2D(
            self.shift.x + self.radius, self.shift.y + self.radius))
        return (pos0.x, pos0.y, pos1.x, pos1.y)
  

class Plank(CanvasSprite, PhysicalSprite):

    def __init__(self, end0, end1, e, app):
        PhysicalSprite.__init__(self, (end0 + end1) / 2.0, Vect2D(0, 0), Vect2D(0, 0), 0)
        CanvasSprite.__init__(self, app)

        self.end0 = end0
        self.end1 = end1
        self.e = e
        self.create_line()

    def _solve_collision(self, obj):
        """ Solve the collision with another ball. """ 
        if obj.__class__ != Ball: return
        seg_u = (self.end1 - self.end0).unit()
        nor_u = Vect2D(-seg_u.y, seg_u.x)
    
        so = obj.shift - self.end0
        xpos = seg_u.dot(so)
        xpos_v = seg_u * xpos
        if xpos < 0 or xpos_v.dot(self.end1 - self.end0 - xpos_v) < 0: return
        
        dis = so.dot(nor_u)
        vo = nor_u.dot(obj.velo)

        if (nor_u * vo).dot(so - xpos_v) < 0 and abs(dis) - obj.radius < EPS:
            vo1 = -self.e * vo
            
            obj.velo += nor_u * (vo1 - vo)

            #######################
            obj.shift += nor_u * (obj.radius * (1 if dis > 0 else -1) - dis)
  #          obj.canvas_refresh(obj.id, obj.get_vertexes())
            obj.solve_collision()
            ######## fix ##########

    def get_vertexes(self):
        """ Get current position of the plank. """
        ed0 = self.app.trans(self.end0)
        ed1 = self.app.trans(self.end1)
        return (ed0.x, ed0.y, ed1.x, ed1.y)

