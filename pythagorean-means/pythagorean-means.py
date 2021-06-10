from manimlib.imports import *

class PythagoreanMeans(Scene):
    CONFIG = {
        "AB_PROPORTION": 0.25,
        "LINE_LENGTH": 7,
        "COMPASS_RUN_TIME": 2,
    }
    def construct(self):
        self.get_lines()
        self.get_arithmetic_mean()
        self.draw_semicircular_arc()
        self.get_quadratic_mean()
        self.get_geometric_mean()
        self.animate_gm_formula()
        self.get_harmonic_mean()
        self.label_pythagorean_means()

    def get_lines(self):
        self.a = Line(ORIGIN, [self.LINE_LENGTH/(1.+self.AB_PROPORTION),0.,0.])
        self.b = Line(self.a.get_end(), [self.LINE_LENGTH,0.,0.])
        self.lines = VGroup(self.a, self.b)
        self.lines.move_to([0.,0.,0.])

        # Add braces and labels
        self.brace_a = Brace(self.a, DOWN, buff = SMALL_BUFF)
        self.brace_b = Brace(self.b, DOWN, buff = SMALL_BUFF)
        self.label_a = self.brace_a.get_tex('a')
        self.label_b = self.brace_b.get_tex('b')
        self.labels = VGroup(
            self.brace_a, self.brace_b,
            self.label_a, self.label_b
        )

        # Animate lines and labels
        self.play(ShowCreation(self.a))
        self.play(GrowFromCenter(self.brace_a), FadeIn(self.label_a))
        self.wait()
        self.play(ShowCreation(self.b), GrowFromCenter(self.brace_b),
            FadeIn(self.label_b)
        )
        self.wait()

    def get_arithmetic_mean(self):
        # Setup line and labels
        self.am_line = Line(
            self.a.get_start(), self.lines.get_center(),
            color = RED_A)
        self.brace_am = Brace(self.am_line, UP, buff = SMALL_BUFF)
        self.brace_am.set_color(RED_A)
        self.label_mean = self.brace_am.get_tex(r'\frac{a+b}{2}')
        self.label_mean.set_color(RED_A)
        self.label_am = self.brace_am.get_text(r'AM')
        self.label_am.set_color(RED_A)
        label_copy = self.label_am.copy()
        self.arithmetic_mean = TextMobject(r'AM', r' = arithmetic mean')
        self.arithmetic_mean.set_color(RED_A)
        self.arithmetic_mean.to_edge(LEFT)
        self.arithmetic_mean.shift(1.25*DOWN + SMALL_BUFF*RIGHT)

        # Animate
        self.play(ShowCreation(self.am_line))
        self.play(GrowFromCenter(self.brace_am), Write(self.label_mean))
        self.wait()
        self.play(ReplacementTransform(self.label_mean, self.label_am))
        self.wait()
        self.play(ApplyMethod(label_copy.move_to, self.arithmetic_mean[0]))
        self.add(self.arithmetic_mean[0])
        self.remove(label_copy)
        self.play(Write(self.arithmetic_mean[1]))
        self.wait(2)
        self.play(FadeOut(self.label_am), FadeOut(self.brace_am))

    def draw_semicircular_arc(self):
        tip = Dot(color = YELLOW)
        tip.move_to(self.am_line.get_start())
        self.semicircle = Arc(
            radius = self.LINE_LENGTH/2, start_angle = 0, angle=TAU/2
        ).flip()

        def update_tip(tip):
            tip.move_to(self.semicircle.get_points()[-1])
            return tip

        def update_radius(radius):
            radius.put_start_and_end_on(
                self.semicircle.get_points()[-1], ORIGIN
            )
            return radius

        self.play(FadeIn(tip))
        self.play(
            ShowCreation(self.semicircle),
            UpdateFromFunc(tip, update_tip),
            UpdateFromFunc(self.am_line, update_radius),
            run_time = self.COMPASS_RUN_TIME
        )
        self.play(FadeOut(tip))
        self.add(self.semicircle)
        self.play(Rotating(self.am_line, radians = TAU/4,
            about_point = ORIGIN, run_time = 1, rate_func=smooth))
        self.wait()

    def get_quadratic_mean(self):
        # Setup lines, labels, and braces
        self.qm_line = Line(self.am_line.get_start(),
            self.b.get_start()
            ).set_color(YELLOW)
        diff_line = Line(self.am_line.get_end(),
            self.b.get_start()
            ).set_color(BLUE)
        brace_diff = Brace(diff_line, DOWN,
            buff = 4*SMALL_BUFF).set_color(BLUE)
        label_diff = brace_diff.get_tex(
            r'\dfrac{a+b}{2}', '-b').set_color(BLUE)
        new_label_diff = brace_diff.get_tex(r'\dfrac{a-b}{2}').set_color(BLUE)
        # Animate
        self.play(ShowCreation(self.qm_line))
        self.wait()
        self.play(FadeIn(diff_line))
        self.play(GrowFromCenter(brace_diff), Write(label_diff))
        self.wait(1.5)
        self.play(ReplacementTransform(label_diff, new_label_diff))
        self.wait(2)
        self.play(FadeOut(brace_diff), FadeOut(new_label_diff))
        self.add(self.semicircle)

        # Setup formula animation
        qm_slope = self.qm_line.get_slope()
        brace_qm = Brace(
            self.qm_line,
            (UP-RIGHT*qm_slope)/(1.+ qm_slope**2),
            buff = SMALL_BUFF
        ).set_color(YELLOW)
        label_qm = brace_qm.get_text('QM').set_color(YELLOW)
        label_qm.move_to(brace_qm.get_center() + (1+SMALL_BUFF)*RIGHT/2)
        label_copy = label_qm.copy()
        avg = r'\dfrac{a+b}{2}'
        half_diff = r'\dfrac{a-b}{2}'

        qm = TexMobject(r'\text{QM}')
        qm.set_color(YELLOW)
        qm.move_to(3*DOWN+2*LEFT)

        rhs_1 = TexMobject(
            r'=\sqrt{\left(%s\right)^2+\left(%s\right)^2}' % (avg, half_diff)
        )
        rhs_1.set_color(YELLOW)
        rhs_1.next_to(qm, RIGHT)
        rhs_1.shift(SMALL_BUFF*UP)

        rhs_intermediate = TexMobject(
            r'=\sqrt{%s + %s}' % (
                r'\dfrac{a^2 + b^2 + 2ab}{4}',
                r'\dfrac{a^2 + b^2 - 2ab}{4}'
            )
        )
        rhs_intermediate.set_color(YELLOW)
        rhs_intermediate.next_to(qm, RIGHT)
        rhs_intermediate.shift(SMALL_BUFF*UP)

        rhs_final = TexMobject(
            r'=\sqrt{{{a^2 + b^2} \over 2}}'
        ).set_color(YELLOW)
        rhs_final.next_to(qm, RIGHT)
        rhs_final.shift(SMALL_BUFF*UP)

        # Get individual pieces of above equations
        square_roots = VGroup(VGroup(*[rhs_1[0][i] for i in [1,2]]),
            VGroup(*[rhs_intermediate[0][i] for i in [1,2]]))
        term_1 = VGroup(VGroup(*[rhs_1[0][i] for i in range(3,11)]),
            VGroup(*[rhs_intermediate[0][i] for i in range(3,14)]))
        minuses = VGroup(rhs_1[0][11], rhs_intermediate[0][14])
        term_2 = VGroup(VGroup(*[rhs_1[0][i] for i in range(12,20)]),
            VGroup(*[rhs_intermediate[0][i] for i in range(15,26)]))

        self.quad_formula = TextMobject(
            r'QM', ' = quadratic mean'
        ).set_color(YELLOW)
        self.quad_formula.to_edge(LEFT)
        self.quad_formula.shift(DOWN * 2 + RIGHT * SMALL_BUFF)

        # Animate
        self.play(FadeIn(label_qm))
        self.wait()
        self.play(ApplyMethod(label_copy.move_to, qm))
        self.play(ReplacementTransform(label_copy, qm))
        self.play(Write(rhs_1))
        self.wait()
        items = [square_roots, term_1, minuses, term_2]
        self.play(*[ReplacementTransform(item[0], item[1]) for item in items],
            ReplacementTransform(rhs_1[0][0], rhs_intermediate[0][0])
        )
        self.wait(2)
        qm_final = VGroup(*rhs_final[0][3:])
        square_root_final = VGroup(rhs_final[0][1], rhs_final[0][2])
        num_copies = VGroup(term_1[1][0:5].copy(), term_2[1][0:5].copy())
        denom_copies = VGroup(term_1[1][9:].copy(), term_2[1][9:].copy())
        self.play(
            FadeOut(rhs_intermediate),
            ApplyMethod(num_copies[1].move_to,
                VGroup(*rhs_final[0][3:8]).get_center()
            ),
            ReplacementTransform(
                num_copies[0], VGroup(*rhs_final[0][3:8])
            ),
            ReplacementTransform(
                denom_copies, VGroup(*rhs_final[0][8:])
            ),
            ReplacementTransform(square_roots[1], square_root_final),
            ReplacementTransform(rhs_intermediate[0][0], rhs_final[0][0])
        )
        self.play(FadeOut(num_copies[1]))
        self.wait()
        self.play(ApplyMethod(qm.move_to, self.quad_formula[0].get_center()),
            FadeOut(rhs_final))
        self.play(Write(self.quad_formula[1]))
        self.play(FadeOut(diff_line), FadeOut(label_qm))
        self.wait(2)

    def get_geometric_mean(self):
        # Setup lines
        gm_length = (self.a.get_length() * self.b.get_length())**0.5
        self.gm_line = Line(self.b.get_start(),
            self.b.get_start()+[0., gm_length, 0.], color = TEAL)
        self.radius = Line(self.am_line.get_end(), self.gm_line.get_end())

        # Animate
        self.play(ShowCreation(self.gm_line))
        self.add(self.semicircle)
        [self.add(line) for line in [self.a, self.b]]
        self.wait()
        self.play(ShowCreation(self.radius))
        self.wait()

    def animate_gm_formula(self):
        # Setup Tex and Text
        brace_gm = Brace(self.gm_line, RIGHT, buff = SMALL_BUFF).set_color(TEAL)
        label_gm = brace_gm.get_tex(r'{\rm GM}').set_color(TEAL)
        label_gm.bg=BackgroundRectangle(label_gm, fill_opacity=0.9)
        label_copy = label_gm.copy()
        label_gm_group = VGroup(label_gm.bg, label_gm)
        avg = r'\dfrac{a+b}{2}'
        half_diff = r'\dfrac{a-b}{2}'

        gm = TexMobject(r'\text{GM}')
        gm.set_color(TEAL)
        gm.move_to(3*DOWN+2*LEFT)

        rhs_1 = TexMobject(
            r'=\sqrt{\left(%s\right)^2-\left(%s\right)^2}' % (avg, half_diff)
        )
        rhs_1.set_color(TEAL)
        rhs_1.next_to(gm, RIGHT)
        rhs_1.shift(SMALL_BUFF*UP)

        rhs_intermediate = TexMobject(
            r'=\sqrt{%s - %s}' % (
                r'\dfrac{a^2 + b^2 + 2ab}{4}',
                r'\dfrac{a^2 + b^2 - 2ab}{4}'
            )
        )
        rhs_intermediate.set_color(TEAL)
        rhs_intermediate.next_to(gm, RIGHT)
        rhs_intermediate.shift(SMALL_BUFF*UP)

        rhs_final = TexMobject(r'=\sqrt{ab}').set_color(TEAL)
        rhs_final.next_to(gm, RIGHT)
        rhs_final.shift(SMALL_BUFF*UP/2)

        # Get individual pieces of above equations
        square_roots = VGroup(VGroup(*[rhs_1[0][i] for i in [1,2]]),
            VGroup(*[rhs_intermediate[0][i] for i in [1,2]]))
        term_1 = VGroup(VGroup(*[rhs_1[0][i] for i in range(3,11)]),
            VGroup(*[rhs_intermediate[0][i] for i in range(3,14)]))
        minuses = VGroup(rhs_1[0][11], rhs_intermediate[0][14])
        term_2 = VGroup(VGroup(*[rhs_1[0][i] for i in range(12,20)]),
            VGroup(*[rhs_intermediate[0][i] for i in range(15,26)]))

        self.gm_formula = TextMobject(
            'GM', r' = geometric mean'
        ).set_color(TEAL)
        self.gm_formula.to_edge(LEFT)
        self.gm_formula.shift(2.75*DOWN + SMALL_BUFF * RIGHT)

        # Animate
        self.play(GrowFromCenter(brace_gm), FadeIn(label_gm_group))
        self.wait()
        self.play(ApplyMethod(label_copy.move_to, gm))
        self.add(gm)
        self.remove(label_copy)
        self.play(Write(rhs_1))
        self.wait()
        items = [square_roots, term_1, minuses, term_2]
        self.play(*[ReplacementTransform(item[0], item[1]) for item in items],
            ReplacementTransform(rhs_1[0][0], rhs_intermediate[0][0]))
        self.wait(2)
        ab_final = VGroup(rhs_final[0][-1], rhs_final[0][-2])
        square_root_final = VGroup(rhs_final[0][1], rhs_final[0][2])
        ab_copies = VGroup(
            *[VGroup(term[1][-3], term[1][-4]) for term in [term_1, term_2]]
        ).copy()
        self.play(
            FadeOut(rhs_intermediate),
            *[ApplyMethod(ab.move_to, ab_final) for ab in ab_copies],
            ReplacementTransform(square_roots[1], square_root_final),
            ReplacementTransform(rhs_intermediate[0][0], rhs_final[0][0])
        )
        self.wait(2)
        self.play(ApplyMethod(gm.move_to, self.gm_formula[0].get_center()),
            FadeOut(rhs_final), FadeOut(ab_copies))
        self.play(Write(self.gm_formula[1]))
        self.play(FadeOut(brace_gm), FadeOut(label_gm_group))
        self.wait(2)

    def get_harmonic_mean(self):
        # Setup lines and formulae
        d1 = Dot()
        harmonic_mean = 2./(1/self.a.get_length() + 1/self.b.get_length())
        avg = (self.a.get_length() + self.b.get_length())/2
        d1.move_to(self.radius.get_end()*(1.-harmonic_mean/avg))
        intersecting_line = Line(d1.get_center(), self.gm_line.get_start())
        intersecting_triangle = Polygon(
            *[point for point in [intersecting_line.get_start_and_end()[0],
                intersecting_line.get_start_and_end()[1], ORIGIN]],
            color=WHITE
        )
        right_angle = RightAngle(intersecting_line, self.radius,
            length = self.LINE_LENGTH/32., quadrant = (1,-1)
        )
        self.hm_line = Line(d1.get_center(),
            self.gm_line.get_end(), color = PINK
        )
        self.hm_formula = TextMobject(
            'HM', r' = harmonic mean'
        ).set_color(PINK)
        self.hm_formula.to_edge(LEFT)
        self.hm_formula.shift(3.5*DOWN + SMALL_BUFF * RIGHT)

        prop_form = TexMobject(
            r'{ {\rm HM} \over {\rm GM} }',
            '=', r'{ {\rm GM} \over {\rm AM} }'
        )
        HM = VGroup(prop_form[0][0], prop_form[0][1])
        gm_denom = VGroup(prop_form[0][-1], prop_form[0][-2])
        gm_num = VGroup(prop_form[2][0], prop_form[2][1])
        am_denom = VGroup(prop_form[2][-1], prop_form[2][-2])
        GM2 = TexMobject(r'{\rm GM}','^2')
        GM2[0].set_color(TEAL)

        prop_form.shift(2*DOWN + 2*RIGHT)
        HM.set_color(PINK)
        gm_num.set_color(TEAL)
        gm_denom.set_color(TEAL)
        am_denom.set_color(RED_A)

        # Animate
        self.play(
            ShowCreation(intersecting_line),
            ShowCreation(right_angle)
        )
        self.wait()
        self.play(ShowCreation(self.hm_line))
        self.add(self.semicircle)
        self.play(FadeIn(intersecting_triangle))
        lines = [self.hm_line, self.gm_line, self.gm_line, self.radius]
        dests = [HM, gm_denom, gm_num, am_denom]
        for line, dest in zip(lines, dests):
            self.play(ReplacementTransform(line.copy(), dest))
        self.play(
            Write(prop_form[0][2]),
            Write(prop_form[1]),
            Write(prop_form[2][2])
        )
        self.wait(2)
        self.play(
            ApplyMethod(gm_denom.move_to, gm_num)
        )
        GM2.move_to(gm_num[1].get_center()+SMALL_BUFF*LEFT)
        GM2 = VGroup(gm_num, GM2[1])
        self.remove(gm_denom)
        self.play(Write(GM2[1]))
        self.play(ApplyMethod(HM.move_to, prop_form[0][2].get_center()),
            FadeOut(prop_form[0][2])
        )
        self.wait()
        equals = TexMobject(r'= {2ab \over {a+b}}')
        equals.next_to(HM)
        num = VGroup(*[equals[0][i] for i in [2,3]]).set_color(TEAL)
        denom = VGroup(*[equals[0][i] for i in [1,-1,-2,-3]]).set_color(RED_A)
        self.play(
            ReplacementTransform(GM2, num),
            ReplacementTransform(prop_form[2][2], equals[0][4]),
            ReplacementTransform(prop_form[1], equals[0][0])
        )
        self.play(ReplacementTransform(am_denom, denom))
        self.wait()
        denom = VGroup(equals[0][-3], equals[0][-2], equals[0][-1])
        hm_denom = TexMobject(
            r'{1 \over a}', '+', r'{1 \over b}'
        ).set_color(PINK)
        hm_denom.next_to(equals[0][4], DOWN)
        self.play(*[ApplyMethod(
                denom[i].move_to, hm_denom[i][-1]
            ) for i in range(3)]
        )
        self.play(Write(hm_denom), FadeOut(equals[0][2]), FadeOut(equals[0][3]),
            ApplyMethod(equals[0][1].next_to, equals[0][4], UP, buff = 0)
        )
        self.play(*[ApplyMethod(
                equals[0][i].set_color, PINK
            ) for i in [0, 1, 4]])
        self.play(*[FadeOut(denom[i]) for i in range(3)])
        self.wait(2)
        self.play(ApplyMethod(HM.move_to, self.hm_formula[0]),
            *[FadeOut(item) for item in [hm_denom, equals[0][0],
                equals[0][1], equals[0][4]]])
        self.play(Write(self.hm_formula[1]))
        self.wait(2)

    def label_pythagorean_means(self):
        form_group = VGroup(self.arithmetic_mean, self.quad_formula,
            self.gm_formula, self.hm_formula
        )
        # Make brace so it is drawn top-to-bottom
        form_brace = Brace(
            form_group, LEFT, buff = SMALL_BUFF
        ).flip().next_to(form_group, RIGHT)
        form_label = form_brace.get_text('Pythagorean means')

        self.play(Write(form_brace))
        self.play(Write(form_label))
        self.wait(4)
