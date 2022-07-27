# from manimlib.imports import *
from manim import *

class VoyagerHydrogen(Scene):
    def construct(self):
        self.camera.frame_height = 2 * self.camera.frame_height / 3
        self.camera.frame_width = 2 * self.camera.frame_width / 3
        stroke_color = '#ffffaa'
        radius = 1.5
        circle = Circle(radius=radius, color=stroke_color)
        # spin_up = Rectangle(height=radius/3, width=1/24)
        spin_up = Line(color=stroke_color).rotate(90*DEGREES)
        spin_up.set_length(radius/3)
        up_circle = Dot(color=stroke_color, stroke_width=0, stroke_color='#00000000')
        up_circle.next_to(spin_up, UP, buff=-0.01)
        spin_up = VGroup(up_circle, spin_up)
        # spin_up = Union(up_circle, spin_up, color=stroke_color, stroke_width=0, fill_opacity=1.)
        spin_down = spin_up.copy()
        spin_down.rotate(180*DEGREES)
        proton = spin_up.copy()
        proton.move_to(circle.get_center())
        spin_down.move_to(circle.point_at_angle(90*DEGREES))
        spin_up.move_to(circle.point_at_angle(90*DEGREES))

        h1 = VGroup(circle, proton)
        h2 = h1.copy()

        VGroup(h1, spin_down).shift(2.5*LEFT)
        VGroup(h2, spin_up).shift(2.5*RIGHT)

        line = Line(color=stroke_color)
        line.set_length(1.75)
        one = Line(color=stroke_color)
        one.set_length(0.167)
        one.rotate(90*DEGREES).shift(0.167*DOWN)

        # self.play(
        #     FadeIn(VGroup(h1, spin_down, h2, spin_up, line, one))
        #     )
        self.add(h1, spin_down, h2, spin_up, line, one)
        self.wait(.75)
        self.play(
            Rotate(spin_up, 180*DEGREES)
            , Rotate(spin_down, 180*DEGREES)
            , run_time=.5
            )
        self.wait(.75)
        self.play(
            Rotate(spin_up, -180*DEGREES)
            , Rotate(spin_down, -180*DEGREES)
            , run_time=.5
            )

class VoyagerHydrogenBW(Scene):
    def construct(self):
        # Atom 1
        stroke_color = BLACK
        self.camera.background_color = WHITE
        radius = 1.5
        circle = Circle(radius=radius, color=stroke_color)
        spin_up = Line(color=stroke_color).rotate(90*DEGREES)
        spin_up.set_length(radius/3)
        up_circle = Dot(color=stroke_color)
        up_circle.next_to(spin_up, UP, buff=0.)
        spin_up = VGroup(up_circle, spin_up)
        spin_down = spin_up.copy()
        spin_down.rotate(180*DEGREES)
        proton = spin_up.copy()
        proton.move_to(circle.get_center())
        spin_down.move_to(circle.point_at_angle(90*DEGREES))
        spin_up.move_to(circle.point_at_angle(90*DEGREES))

        h1 = VGroup(circle, proton)
        h2 = h1.copy()

        VGroup(h1, spin_down).shift(2.5*LEFT)
        VGroup(h2, spin_up).shift(2.5*RIGHT)

        line = Line(color=stroke_color)
        line.set_length(1.75)
        one = Line(color=stroke_color)
        one.set_length(0.167)
        one.rotate(90*DEGREES).shift(0.167*DOWN)

        # self.play(
        #     FadeIn(VGroup(h1, spin_down, h2, spin_up, line, one))
        #     )
        self.add(h1, spin_down, h2, spin_up, line, one)
        self.wait(.75)
        self.play(
            Rotate(spin_up, 180*DEGREES)
            , Rotate(spin_down, 180*DEGREES)
            , run_time=.5
            )
        self.wait(.75)
        self.play(
            Rotate(spin_up, -180*DEGREES)
            , Rotate(spin_down, -180*DEGREES)
            , run_time=.5
            )
