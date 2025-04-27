from manim import *
import numpy as np


LIGHT_GREEN = "#95C05C"
PINK = "#EA337F"
LIGHT_BLUE = "#4EADEA"


class FieldEquation(Scene):
    def construct(self):
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage{cancel}")

        self.camera.frame_width = 16
        self.camera.frame_height = 9

        equation = MathTex(
            r"B(x, y, z) = (",
            r"B_0",
            r"+",
            r"G_z z",
            r"+",
            r"G_y y",
            r"+",
            r"G_x x",
            r")",
            r"\hat{z}", tex_template=tex_template
        )

        equation[1].set_color(RED)  # B_0
        equation[3].set_color(LIGHT_GREEN)  # z gradient
        equation[5].set_color(PINK)  # y gradient
        equation[7].set_color(LIGHT_BLUE)  # x gradient
        equation[9].set_color(PURPLE)  # z hat

        # equation[5].set_opacity(0.6)
        # equation[7].set_opacity(0.6)

        self.add(equation)


class LarmorFrequencyEquation(Scene):
    def construct(self):
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        equation = MathTex(
            r"\omega _{Larmor}",
            r"=",
            r"\gamma",
            r"B(x, y, z)"
        )

        equation[0].set_color(LIGHT_BLUE)
        equation[2].set_color(PINK)
        # equation[3].set_color(LIGHT_GREEN)

        self.add(equation)


class SliceSelectionGraph(Scene):
    def construct(self):
        # Set the camera dimensions
        self.camera.frame_width = 16
        self.camera.frame_height = 9
        self.camera.background_color = WHITE

        # Create w-z axes (swapped as requested)
        w_z_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "include_ticks": False,
                "color": BLACK
            },
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT},
            x_length=5,
            y_length=5
        ).scale(0.6)

        # Position the top axes
        w_z_axes.to_edge(UP, buff=1)

        # Add labels for the axes (swapped z and w)
        w_label = MathTex("\\omega", color=BLACK).next_to(w_z_axes.x_axis.get_end(), DOWN)
        z_label = MathTex("z", color="BLACK").next_to(w_z_axes.y_axis.get_end(), LEFT)

        # Create the gradient line (linear mapping from w to z)
        gradient_line = w_z_axes.plot(lambda x: x, x_range=[0, 5], color=LIGHT_GREEN)
        gradient_line_label = MathTex("G_z", color=LIGHT_GREEN).next_to(gradient_line, RIGHT, buff=-0.2)

        # Create second axes for RF pulse
        rf_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[-1.2, 1.2, 0.5],  # Changed to accommodate both positive and negative values
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "include_ticks": False,
                "color": BLACK
            },
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT},
            x_length=5,
            y_length=3  # Shorter y-axis for the amplitude
        ).scale(0.6)

        # Position the RF pulse axes below the first graph
        rf_axes.to_edge(DOWN, buff=1)

        # Align the RF pulse graph with the first graph horizontally
        rf_axes.align_to(w_z_axes, LEFT)

        # Add labels for the RF pulse graph
        rf_w_label = MathTex("\\omega", color=BLACK).next_to(rf_axes.x_axis.get_end(), DOWN)
        amplitude_label = MathTex("Amplitude", color=BLACK).next_to(rf_axes.y_axis.get_end(), LEFT)

        # Define key points for slice selection
        z_0 = 2.5  # Center of the slice
        delta_z = 1.0  # Width of the slice

        # Since z = w in our mapping, these values are the same
        w_0 = z_0
        delta_w = delta_z

        # Define slice boundaries
        z_min = z_0 - delta_z / 2
        z_max = z_0 + delta_z / 2
        w_min = w_0 - delta_w / 2
        w_max = w_0 + delta_w / 2

        # Add tick mark for z_0
        z_0_tick = Line(
            w_z_axes.c2p(0, z_0) + LEFT * 0.1,
            w_z_axes.c2p(0, z_0) + RIGHT * 0.1,
            color=RED
        )
        z_min_tick = Line(
            w_z_axes.c2p(0, z_min) + LEFT * 0.1,
            w_z_axes.c2p(0, z_min) + RIGHT * 0.1,
            color=BLUE
        )
        z_max_tick = Line(
            w_z_axes.c2p(0, z_max) + LEFT * 0.1,
            w_z_axes.c2p(0, z_max) + RIGHT * 0.1,
            color=BLUE
        )
        z_0_label = MathTex("z_0", color=BLACK).next_to(z_0_tick, LEFT)

        # Add brace showing delta_z
        delta_z_brace = BraceBetweenPoints(
            w_z_axes.c2p(0, z_min),
            w_z_axes.c2p(0, z_max),
            direction=LEFT,
            buff=0.7,
            color=BLACK
        )
        delta_z_label = MathTex("\\Delta z", color=BLACK).next_to(delta_z_brace, LEFT)

        # Mark the points where the slice boundaries hit the gradient line
        z_min_dot = Dot(w_z_axes.c2p(w_min, z_min), color=BLUE)
        z_max_dot = Dot(w_z_axes.c2p(w_max, z_max), color=BLUE)
        z_center_dot = Dot(w_z_axes.c2p(w_0, z_0), color=RED)

        horizontal_dashed_line_min = DashedLine(
            w_z_axes.c2p(0, z_min),
            w_z_axes.c2p(w_min, z_min),
            color=BLUE,
            dash_length=0.1
        )

        horizontal_dashed_line_max = DashedLine(
            w_z_axes.c2p(0, z_max),
            w_z_axes.c2p(w_max, z_max),
            color=BLUE,
            dash_length=0.1
        )

        horizontal_dashed_line_center = DashedLine(
            w_z_axes.c2p(0, z_0),
            w_z_axes.c2p(w_0, z_0),
            color=RED,
            dash_length=0.1
        )

        # Draw dashed lines to show the frequency range
        dashed_line_min = DashedLine(
            w_z_axes.c2p(w_min, z_min),
            w_z_axes.c2p(w_min, 0),
            color=BLUE,
            dash_length=0.1
        )

        dashed_line_max = DashedLine(
            w_z_axes.c2p(w_max, z_max),
            w_z_axes.c2p(w_max, 0),
            color=BLUE,
            dash_length=0.1
        )

        dashed_line_center = DashedLine(
            w_z_axes.c2p(w_0, z_0),
            w_z_axes.c2p(w_0, 0),
            color=RED,
            dash_length=0.1
        )

        # Mark the frequency range on the w-axis of the top graph
        w_min_tick = Line(
            w_z_axes.c2p(w_min, 0) + DOWN * 0.1,
            w_z_axes.c2p(w_min, 0) + UP * 0.1,
            color=BLUE
        )

        w_max_tick = Line(
            w_z_axes.c2p(w_max, 0) + DOWN * 0.1,
            w_z_axes.c2p(w_max, 0) + UP * 0.1,
            color=BLUE
        )

        w_0_tick = Line(
            w_z_axes.c2p(w_0, 0) + DOWN * 0.1,
            w_z_axes.c2p(w_0, 0) + UP * 0.1,
            color=RED
        )

        # Connect to second graph
        connect_min = DashedLine(
            w_z_axes.c2p(w_min, 0),
            rf_axes.c2p(w_min, 0),
            color=BLUE,
            dash_length=0.1
        )

        connect_max = DashedLine(
            w_z_axes.c2p(w_max, 0),
            rf_axes.c2p(w_max, 0),
            color=BLUE,
            dash_length=0.1
        )

        connect_center = DashedLine(
            w_z_axes.c2p(w_0, 0),
            rf_axes.c2p(w_0, 0),
            color=RED,
            dash_length=0.1
        )

        # Create a wave function that's zero outside the bandwidth and a sinc wave inside
        def wave_function(x):
            import numpy as np
            if w_min <= x <= w_max:
                return 1
            else:
                return 0

        # Plot the wave on the RF pulse axes
        rf_wave = rf_axes.plot(
            wave_function,
            x_range=[0, 5, 0.01],  # Smaller step for smoother curve
            color=PINK,
        )

        # Add a fill below the curve to make it more visible
        rf_fill = rf_axes.get_area(
            rf_wave,
            x_range=[w_min, w_max],
            color=PINK,
            opacity=0.3
        )

        # Add ticks on the second graph
        rf_w_min_tick = Line(
            rf_axes.c2p(w_min, 0) + DOWN * 0.1,
            rf_axes.c2p(w_min, 0) + UP * 0.1,
            color=BLUE
        )

        rf_w_max_tick = Line(
            rf_axes.c2p(w_max, 0) + DOWN * 0.1,
            rf_axes.c2p(w_max, 0) + UP * 0.1,
            color=BLUE
        )

        rf_w_0_tick = Line(
            rf_axes.c2p(w_0, 0) + DOWN * 0.1,
            rf_axes.c2p(w_0, 0) + UP * 0.1,
            color=RED
        )

        rf_delta_w_brace = BraceBetweenPoints(
            rf_axes.c2p(w_min, 0),
            rf_axes.c2p(w_max, 0),
            direction=DOWN,
            color=BLACK
        )
        rf_delta_w_label = MathTex("\\Delta \\omega", color=BLACK).next_to(rf_delta_w_brace, DOWN)

        rf_w_0_label = MathTex("\\omega_0", color=BLACK).next_to(rf_w_0_tick, UP)

        # Add everything to the scene
        self.add(
            # Top graph elements
            w_z_axes, z_label, w_label, gradient_line,
            z_0_tick, z_0_label, delta_z_brace, delta_z_label,
            z_min_dot, z_max_dot, z_center_dot,
            dashed_line_min, dashed_line_max, dashed_line_center,
            w_min_tick, w_max_tick, w_0_tick, z_max_tick, z_min_tick,
            horizontal_dashed_line_min, horizontal_dashed_line_max,
            horizontal_dashed_line_center, gradient_line_label,

            # Connecting lines
            connect_min, connect_max, connect_center,

            # Bottom graph elements
            rf_axes, rf_w_label, amplitude_label,
            rf_wave, rf_fill,
            rf_w_min_tick, rf_w_max_tick, rf_w_0_tick,
            rf_delta_w_brace, rf_delta_w_label, rf_w_0_label
        )


class SliceSelectionAnimation(Scene):
    def construct(self):
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        brain_image = ImageMobject("assets/brain-sagittal")
        # brain_image.rotate(90 * DEGREES)
        brain_image.scale_to_fit_height(7)
        self.add(brain_image)

        # Add a semi-transparent overlay to improve spin visibility
        brain_overlay = Rectangle(
            width=brain_image.width,
            height=brain_image.height,
            fill_color=BLACK,
            fill_opacity=0.2,
            stroke_opacity=0
        )
        brain_overlay.move_to(brain_image.get_center())
        self.add(brain_overlay)

        num_rows = 15
        num_cols = 7

        initial_angle = 30 * DEGREES
        starting_animation_duration = 5
        gradient_animation_duration = 5

        spin_speed_up_factor = 2

        base_frequency = 1.0

        brain_center = brain_image.get_center()
        brain_width = brain_image.width
        brain_height = brain_image.height

        def is_within_brain(x, y):
            rel_x = x - brain_center[0]
            rel_y = y - brain_center[1]

            norm_x = rel_x / (brain_width / 2)
            norm_y = rel_y / (brain_height / 2)

            return (norm_x ** 2 / 0.7 ** 2 + norm_y ** 2 / 0.9 ** 2) < 1

        all_spins = []
        spin_positions = []

        base_spin_anims = []

        for row in range(num_rows):
            for col in range(num_cols):
                x = (col - (num_cols - 1) / 2) * 0.8 + brain_center[0]
                y = (row - (num_rows - 1) / 2) * 0.8 + brain_center[1]

                # Skip positions that are outside the brain
                if not is_within_brain(x, y):
                    continue

                spin_circle = Circle(radius=0.1, color=WHITE)
                spin_circle.set_fill(WHITE)

                line = Line([0, -0.25, 0], [0, 0.25, 0], color=LIGHT_GREEN, stroke_width=5)
                arrow_tip = ArrowTriangleFilledTip(color=LIGHT_GREEN).scale(0.5)
                line.add_tip(tip=arrow_tip, at_start=False, tip_length=0.1)

                gradient_factor = (row - (num_rows - 1) / 2) / ((num_rows - 1) / 2)
                precession_frequency = base_frequency + (gradient_factor)
                phase_angle = precession_frequency * TAU

                if 6 <= row <= 7:
                    line.rotate(90 * DEGREES)
                else:
                    line.rotate(initial_angle)
                line.rotate(phase_angle, axis=UP)

                spin_group = VGroup(spin_circle, line)
                spin_group.move_to([x, y, 0])
                self.add(spin_group)

                all_spins.append(spin_group)
                spin_positions.append([row, col, x, y, spin_group])

                anim = Rotate(
                    line,
                    angle=base_frequency * TAU * spin_speed_up_factor,
                    axis=UP,
                    about_point=spin_group.get_center(),
                    rate_func=linear,
                    run_time=starting_animation_duration
                )
                base_spin_anims.append(anim)
        # === Add Z-axis on the left ===
        z_axis = NumberLine(
            x_range=[0, num_rows - 1, 1],
            length=7,
            rotation=PI / 2,
            include_tip=True,
            label_direction=UP,
            color=BLACK
        )
        z_axis.next_to(brain_image, LEFT)
        z_label = MathTex("z", color=BLACK, font_size=36)
        z_label.next_to(z_axis, LEFT).shift(UP * 3)

        # Mark z_0 (middle slice)
        z_0_index = num_rows // 2 - 0.5
        z_0_value = z_axis.number_to_point(z_0_index)[1]
        z_0_marker = Dot(z_axis.number_to_point(z_0_index), color=YELLOW)
        z_0_label = MathTex("z_0", font_size=36, color=YELLOW)
        z_0_label.next_to(z_0_marker, LEFT)

        self.add(z_axis, z_label, z_0_marker, z_0_label)

        # === Add Overlay Rectangle for z_0 Slice ===
        overlay_height = 0.8 * 2  # Two rows tall
        overlay_width = brain_image.width
        overlay_rect = Rectangle(
            width=overlay_width,
            height=overlay_height,
            fill_color=YELLOW,
            fill_opacity=0.3,
            stroke_color=YELLOW,
            stroke_width=2
        )

        z_0_y = (z_0_index - (num_rows - 1) / 2) * 0.8 + brain_center[1]
        overlay_rect.move_to([brain_center[0], z_0_y, 0])
        self.add(overlay_rect)

        # self.play(*base_spin_anims)
        #
        # # Gradient Application
        gradient_arrow = Arrow(start=np.array([4, -3, 0]), end=np.array([4, 3, 0]), buff=0.1, color=LIGHT_BLUE)
        gradient_label = MathTex("G_z", color=LIGHT_BLUE, font_size=48)
        gradient_label.next_to(gradient_arrow, RIGHT, buff=0.1)
        #
        # self.play(Create(gradient_arrow), Write(gradient_label), run_time=0.5)
        # self.add(gradient_arrow, gradient_label)

        omega_small = MathTex(r"\downarrow \omega", color=LIGHT_GREEN, font_size=36)
        omega_large = MathTex(r"\uparrow \omega", color=LIGHT_GREEN, font_size=60)

        omega_large.next_to(brain_image, UP).shift(DOWN).shift(RIGHT * 2.7)
        omega_small.next_to(brain_image, DOWN).shift(UP).shift(RIGHT * 2.7)

        # self.add(omega_small, omega_large)
        #
        # precession_anims = []
        #
        # for row, col, x, y, spin_group in spin_positions:
        #     arrow = spin_group[1]
        #
        #     gradient_factor = (row - (num_rows - 1) / 2) / ((num_rows - 1) / 2)
        #     precession_frequency = base_frequency + (gradient_factor * 0.5)
        #     rotation_angle = precession_frequency * TAU
        #
        #     anim = Rotate(
        #         arrow,
        #         angle=rotation_angle * spin_speed_up_factor,
        #         axis=UP,
        #         about_point=spin_group.get_center(),
        #         rate_func=linear,
        #         run_time=gradient_animation_duration
        #     )
        #     precession_anims.append(anim)
        #
        # self.play(*precession_anims)


class SliceSelectionRephasingAnimation(Scene):
    def construct(self):
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        brain_image = ImageMobject("assets/brain-sagittal")
        # brain_image.rotate(90 * DEGREES)
        brain_image.scale_to_fit_height(7)
        self.add(brain_image)

        # Add a semi-transparent overlay to improve spin visibility
        brain_overlay = Rectangle(
            width=brain_image.width,
            height=brain_image.height,
            fill_color=BLACK,
            fill_opacity=0.2,
            stroke_opacity=0
        )
        brain_overlay.move_to(brain_image.get_center())
        self.add(brain_overlay)

        num_rows = 15
        num_cols = 7

        initial_angle = 30 * DEGREES
        rephasing_animation_duration = 5  # Reverse gradient (half duration)

        spin_speed_up_factor = 2

        base_frequency = 1.0

        brain_center = brain_image.get_center()
        brain_width = brain_image.width
        brain_height = brain_image.height

        def is_within_brain(x, y):
            rel_x = x - brain_center[0]
            rel_y = y - brain_center[1]

            norm_x = rel_x / (brain_width / 2)
            norm_y = rel_y / (brain_height / 2)

            return (norm_x ** 2 / 0.7 ** 2 + norm_y ** 2 / 0.9 ** 2) < 1

        all_spins = []
        spin_positions = []

        # Create all spins
        for row in range(num_rows):
            for col in range(num_cols):
                x = (col - (num_cols - 1) / 2) * 0.8 + brain_center[0]
                y = (row - (num_rows - 1) / 2) * 0.8 + brain_center[1]

                # Skip positions that are outside the brain
                if not is_within_brain(x, y):
                    continue

                spin_circle = Circle(radius=0.1, color=WHITE)
                spin_circle.set_fill(WHITE)

                line = Line([0, -0.25, 0], [0, 0.25, 0], color=LIGHT_GREEN, stroke_width=5)
                arrow_tip = ArrowTriangleFilledTip(color=LIGHT_GREEN).scale(0.5)
                line.add_tip(tip=arrow_tip, at_start=False, tip_length=0.1)

                # Calculate position-dependent phase based on row position
                gradient_factor = (row - (num_rows - 1) / 2) / ((num_rows - 1) / 2)
                precession_frequency = base_frequency + (gradient_factor)
                phase_angle = precession_frequency * TAU

                if 6 <= row <= 7:
                    line.rotate(90 * DEGREES)
                else:
                    line.rotate(initial_angle)
                line.rotate(phase_angle, axis=UP)

                spin_group = VGroup(spin_circle, line)
                spin_group.move_to([x, y, 0])
                self.add(spin_group)

                all_spins.append(spin_group)
                spin_positions.append([row, col, x, y, spin_group, gradient_factor])

        # Start with a gradient arrow showing the dephasing that has already occurred
        gradient_arrow = Arrow(start=np.array([4, -3, 0]), end=np.array([4, 3, 0]), buff=0.1, color=LIGHT_BLUE)
        gradient_label = MathTex("G_z", color=LIGHT_BLUE, font_size=48)
        gradient_label.next_to(gradient_arrow, RIGHT, buff=0.1)
        self.add(gradient_arrow, gradient_label)

        # Wait a moment to observe the dephased state
        self.wait(3)

        # Create and show reverse gradient
        reverse_gradient_arrow = Arrow(start=np.array([4, 3, 0]), end=np.array([4, -3, 0]), buff=0.1, color=RED)
        reverse_gradient_label = MathTex("-G_z", color=RED, font_size=48)
        reverse_gradient_label.next_to(reverse_gradient_arrow, RIGHT, buff=0.1)

        self.play(
            FadeOut(gradient_arrow),
            FadeOut(gradient_label),
            FadeIn(reverse_gradient_arrow),
            FadeIn(reverse_gradient_label),
            run_time=0.5
        )

        # Create animations for rephasing
        rephasing_anims = []

        for row, col, x, y, spin_group, gradient_factor in spin_positions:
            arrow = spin_group[1]

            # Reverse rotation - faster spins now rotate slower and vice versa to catch up
            rephasing_frequency = base_frequency - (gradient_factor * 0.5)
            rotation_angle = rephasing_frequency * TAU

            anim = Rotate(
                arrow,
                angle=rotation_angle * spin_speed_up_factor,
                axis=UP,
                about_point=spin_group.get_center(),
                rate_func=linear,
                run_time=rephasing_animation_duration
            )
            rephasing_anims.append(anim)

        self.play(*rephasing_anims)

        # self.wait(2)

        self.play(
            FadeOut(reverse_gradient_label),
            FadeOut(reverse_gradient_arrow),
            run_time=0.5
        )

        self.wait(4)


class SpinSignalEquations(Scene):
    def construct(self):
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        equation_single_spin = MathTex(
            r"s(t) = ",
            r"M(x, y)",
            r"e^{i \phi ("
            r"t)}"
        ).scale(1.5)

        equation_single_spin[1].set_color(LIGHT_GREEN)

        self.play(Write(equation_single_spin))
        self.wait(3)

        equation_total = MathTex(
            r"s(t) = ",
            r"\int \int",
            r"M(x, y)",
            r"e^{i \phi (",
            r"x,",
            r"y,",
            r"t)}"
            r" \,dx \,dy"
        ).scale(1.5)
        equation_total[2].set_color(LIGHT_GREEN)
        equation_total[4].set_color(PINK)
        equation_total[5].set_color(LIGHT_BLUE)

        self.play(TransformMatchingTex(equation_single_spin, equation_total))
        self.wait(3)


class FrequencyEncoding(Scene):
    def construct(self):
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        brain_image = ImageMobject("assets/brain-axial")
        brain_image.rotate(90 * DEGREES)
        brain_image.scale_to_fit_height(7)
        self.add(brain_image)

        brain_overlay = Rectangle(
            width=brain_image.width,
            height=brain_image.height,
            fill_color=BLACK,
            fill_opacity=0.2,
            stroke_opacity=0
        )
        brain_overlay.move_to(brain_image.get_center())
        self.add(brain_overlay)

        def is_within_brain(x, y):
            rel_x = x - brain_center[0]
            rel_y = y - brain_center[1]

            norm_x = rel_x / (brain_width / 2)
            norm_y = rel_y / (brain_height / 2)

            return (norm_x ** 2 / 0.9 ** 2 + norm_y ** 2 / 0.7 ** 2) < 1

        num_rows = 5
        num_cols = 15

        base_frequency = 1.0
        gradient_strength = 0.7
        spin_duration = 3
        gradient_duration = 3
        animation_speed_up_factor = 1.5

        brain_center = brain_image.get_center()
        brain_width = brain_image.width
        brain_height = brain_image.height

        all_spins = []
        spin_positions = []
        base_spin_anims = []

        for row in range(num_rows):
            for col in range(num_cols):
                x = (col - (num_cols - 1) / 2) * 0.8 + brain_center[0]
                y = (row - (num_rows - 1) / 2) * 0.8 + brain_center[1]

                if not is_within_brain(x, y):
                    continue

                spin_circle = Circle(radius=0.1, color=WHITE, fill_opacity=1)

                arrow = Line([0, -0.25, 0], [0, 0.25, 0], color=LIGHT_GREEN, stroke_width=5)
                arrow_tip = ArrowTriangleFilledTip(color=LIGHT_GREEN).scale(0.5)
                arrow.add_tip(tip=arrow_tip, at_start=False, tip_length=0.1)

                spin_group = VGroup(spin_circle, arrow)
                spin_group.move_to([x, y, 0])
                self.add(spin_group)
                all_spins.append(spin_group)
                spin_positions.append([row, col, x, y, spin_group])

                anim = Rotate(
                    arrow,
                    angle=base_frequency * TAU * animation_speed_up_factor,
                    axis=OUT,
                    about_point=spin_group.get_center(),
                    rate_func=linear,
                    run_time=spin_duration
                )
                arrow.rotate(base_frequency * TAU * animation_speed_up_factor, axis=OUT, about_point=spin_group.get_center())
                base_spin_anims.append(anim)

        # self.play(*base_spin_anims)

        # Gradient Application
        gradient_arrow = Arrow(start=np.array([-4, -3, 0]), end=np.array([4, -3, 0]), buff=0.1, color=LIGHT_BLUE)
        gradient_arrow.next_to(brain_image, DOWN, buff=0.1)
        gradient_label = MathTex("G_x", color=LIGHT_BLUE, font_size=48)
        gradient_label.next_to(gradient_arrow, DOWN, buff=0.1)

        # self.play(Create(gradient_arrow), Write(gradient_label), run_time=0.5)
        self.add(gradient_arrow, gradient_label)

        frequency_anims = []

        for row, col, x, y, spin_group in spin_positions:
            arrow = spin_group[1]

            gradient_factor = (col - (num_cols - 1) / 2) / ((num_cols - 1) / 2)
            frequency = base_frequency + gradient_strength * col
            rotation_angle = frequency * TAU

            anim = Rotate(
                arrow,
                angle=rotation_angle / 2,
                axis=OUT,
                about_point=spin_group.get_center(),
                rate_func=linear,
                run_time=gradient_duration
            )
            arrow.rotate(rotation_angle / 2, axis=OUT, about_point=spin_group.get_center())
            frequency_anims.append(anim)

        omega_small = MathTex(r"\downarrow \omega", color=PINK, font_size=36)
        omega_large = MathTex(r"\uparrow \omega", color=PINK, font_size=60)

        omega_small.next_to(brain_image, LEFT, buff=0.5)
        omega_large.next_to(brain_image, RIGHT, buff=0.5)
        # self.play(Write(omega_small), Write(omega_large))
        self.add(omega_small, omega_large)

        # self.play(*frequency_anims)
        # self.wait(4)


class PhaseEncoding(Scene):
    def construct(self):
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        brain_image = ImageMobject("assets/brain-axial")
        brain_image.rotate(90 * DEGREES)
        brain_image.scale_to_fit_height(7)
        self.add(brain_image)

        brain_overlay = Rectangle(
            width=brain_image.width,
            height=brain_image.height,
            fill_color=BLACK,
            fill_opacity=0.2,
            stroke_opacity=0
        )
        brain_overlay.move_to(brain_image.get_center())
        self.add(brain_overlay)

        brain_center = brain_image.get_center()
        brain_width = brain_image.width
        brain_height = brain_image.height

        def is_within_brain(x, y):
            rel_x = x - brain_center[0]
            rel_y = y - brain_center[1]

            norm_x = rel_x / (brain_width / 2)
            norm_y = rel_y / (brain_height / 2)

            return (norm_x ** 2 / 0.9 ** 2 + norm_y ** 2 / 0.7 ** 2) < 1

        num_rows = 5
        num_cols = 15

        base_frequency = 1.0
        gradient_strength = 1.0
        spin_duration = 3
        gradient_duration = 3
        spin_speed_factor = 2

        all_spins = []
        spin_positions = []
        base_spin_anims = []

        for row in range(num_rows):
            for col in range(num_cols):
                x = (col - (num_cols - 1) / 2) * 0.8 + brain_center[0]
                y = (row - (num_rows - 1) / 2) * 0.8 + brain_center[1]

                if not is_within_brain(x, y):
                    continue

                spin_circle = Circle(radius=0.1, color=WHITE, fill_opacity=1)

                arrow = Line([0, -0.25, 0], [0, 0.25, 0], color=LIGHT_GREEN, stroke_width=5)
                arrow_tip = ArrowTriangleFilledTip(color=LIGHT_GREEN).scale(0.5)
                arrow.add_tip(tip=arrow_tip, at_start=False, tip_length=0.1)

                spin_group = VGroup(spin_circle, arrow)
                spin_group.move_to([x, y, 0])
                self.add(spin_group)
                all_spins.append(spin_group)
                spin_positions.append([row, col, x, y, spin_group])

                anim = Rotate(
                    arrow,
                    angle=base_frequency * TAU * spin_speed_factor,
                    axis=OUT,
                    about_point=spin_group.get_center(),
                    rate_func=linear,
                    run_time=spin_duration
                )
                base_spin_anims.append(anim)
                arrow.rotate(base_frequency * TAU * spin_speed_factor, axis=OUT, about_point=spin_group.get_center())

        # self.play(*base_spin_anims)

        # Gradient Application
        gradient_arrow = Arrow(start=np.array([0, -3, 0]), end=np.array([0, 3, 0]), buff=0.1, color=LIGHT_BLUE)
        gradient_arrow.next_to(brain_image, LEFT, buff=0.1)
        gradient_label = MathTex("G_y", color=LIGHT_BLUE, font_size=48)
        gradient_label.next_to(gradient_arrow, LEFT, buff=0.1)

        # self.play(Create(gradient_arrow), Write(gradient_label), run_time=0.5)
        self.add(gradient_arrow, gradient_label)

        frequency_anims = []

        for row, col, x, y, spin_group in spin_positions:
            arrow = spin_group[1]

            gradient_factor = (row - (num_rows - 1) / 2) / ((num_rows - 1) / 2) + 0.5
            frequency = base_frequency + gradient_strength * gradient_factor
            rotation_angle = frequency * TAU

            anim = Rotate(
                arrow,
                angle=rotation_angle,
                axis=OUT,
                about_point=spin_group.get_center(),
                rate_func=linear,
                run_time=gradient_duration
            )
            frequency_anims.append(anim)
            arrow.rotate(rotation_angle, axis=OUT, about_point=spin_group.get_center())

        # self.play(*frequency_anims)

        # stop gradient
        # self.play(FadeOut(gradient_arrow), FadeOut(gradient_label))
        self.remove(gradient_arrow, gradient_label)

        # all spins precess at the same rate
        all_frequency_anims = []
        for row, col, x, y, spin_group in spin_positions:
            arrow = spin_group[1]

            anim = Rotate(
                arrow,
                angle=base_frequency * 0.875 * TAU * spin_speed_factor,
                axis=OUT,
                about_point=spin_group.get_center(),
                rate_func=linear,
                run_time=spin_duration
            )
            all_frequency_anims.append(anim)
            arrow.rotate(base_frequency * 0.875 * TAU * spin_speed_factor, axis=OUT, about_point=spin_group.get_center())

        # self.play(*all_frequency_anims)

        # self.wait(0.5)

        # Now color-code arrows based on their direction
        LEFT_COLOR = YELLOW
        RIGHT_COLOR = BLUE

        color_change_anims = []

        # First determine arrow directions
        for spin_group in all_spins:
            arrow = spin_group[1]

            # Get the start and end points of the arrow (in global coordinates)
            start_point = arrow.get_start()
            end_point = arrow.get_end()

            # Calculate the direction vector
            direction_vector = np.array(end_point) - np.array(start_point)

            # Check if the arrow is pointing more left or more right
            # If x-component is positive, it's pointing rightward
            is_pointing_right = direction_vector[0] > 0

            new_color = RIGHT_COLOR if is_pointing_right else LEFT_COLOR

            # Create animation to change color
            color_change = ApplyMethod(
                arrow.set_color,
                new_color,
                run_time=0.75
            )

            # Also change the arrow tip color
            for submob in arrow.submobjects:
                if isinstance(submob, ArrowTriangleFilledTip):
                    tip_color_change = ApplyMethod(
                        submob.set_color,
                        new_color,
                        run_time=0.75
                    )
                    color_change_anims.append(tip_color_change)

            color_change_anims.append(color_change)
            arrow.set_color(new_color)
            arrow_tip.set_color(new_color)

        # Play all color change animations simultaneously
        # self.play(*color_change_anims)

        # Now add more rows of spins in between the existing rows
        additional_spins = []
        create_anims = []

        # Create in-between rows (4 additional rows between each original row)
        subrows_per_row = 2
        num_interleaved_rows = num_rows * (subrows_per_row + 1) - subrows_per_row

        small_spin_scale = 0.75  # Smaller size for the additional spins

        # Keeping track of phase across all rows for spatial frequency pattern
        all_row_positions = []
        for row in range(num_interleaved_rows):
            # Calculate the original row number (floating point)
            orig_row = row / (subrows_per_row + 1)
            all_row_positions.append(orig_row)

            # Skip if this was an original row
            if row % (subrows_per_row + 1) == 0:
                continue

            for col in range(num_cols):
                x = (col - (num_cols - 1) / 2) * 0.8 + brain_center[0]
                # Calculate y position for the in-between row
                base_row_spacing = 0.8
                y = (orig_row - (num_rows - 1) / 2) * base_row_spacing + brain_center[1]

                if not is_within_brain(x, y):
                    continue

                # Create smaller spin
                spin_circle = Circle(radius=0.08 * small_spin_scale, color=WHITE, fill_opacity=1)

                # Calculate the appropriate phase for this row based on spatial frequency of 2.5
                # Normalize row position from 0 to 1
                norm_row_pos = (orig_row - 0) / (num_rows - 1)
                # Complete 2.5 cycles over the entire height
                phase_angle = - (2 * TAU * norm_row_pos - PI / 2)

                arrow = Line([0, -0.25 * small_spin_scale, 0],
                             [0, 0.25 * small_spin_scale, 0],
                             stroke_width=4 * small_spin_scale)

                arrow_tip = ArrowTriangleFilledTip().scale(0.5 * small_spin_scale)
                arrow.add_tip(tip=arrow_tip, at_start=False, tip_length=0.1 * small_spin_scale)

                # Rotate the arrow to match the phase
                arrow.rotate(phase_angle, axis=OUT)

                # Get the start and end points of the arrow (in global coordinates)
                start_point = arrow.get_start()
                end_point = arrow.get_end()

                # Calculate the direction vector
                direction_vector = np.array(end_point) - np.array(start_point)

                # Calculate the angle in the X-Y plane (in radians)
                angle = np.arctan2(direction_vector[0], direction_vector[1])

                # Normalize the angle to be between 0 and 1 for color interpolation
                # Map -π to π range to 0 to 1 range
                normalized_angle = (angle + np.pi) / (2 * np.pi)

                # Create a color gradient between LEFT_COLOR and RIGHT_COLOR based on the angle
                # Using color_gradient to get a smooth transition
                arrow_color = interpolate_color(LEFT_COLOR, RIGHT_COLOR, normalized_angle)

                arrow.set_color(arrow_color)
                arrow_tip.set_color(arrow_color)

                spin_group = VGroup(spin_circle, arrow)
                spin_group.move_to([x, y, 0])

                additional_spins.append(spin_group)
                create_anims.append(FadeIn(spin_group, scale=1.2))
                self.add(spin_group)

        # Create animation to display additional spins
        # self.play(*create_anims, run_time=1.5)


        # Add a label for spatial frequency
        freq_label = MathTex(r"\text{Spatial Frequency: } 2 \text{ cycles}", font_size=36)
        freq_label.set_color(LIGHT_BLUE)
        freq_label.to_edge(UP)
        # self.play(FadeIn(freq_label))
        self.add(freq_label)

        # self.wait(1)

    def save_final_frame_as_png(self):
        """
        Save the final frame of the animation as a transparent PNG
        """
        import os
        from PIL import Image
        import numpy as np
        from pathlib import Path

        # Get the current output directory path
        output_dir = Path(os.environ.get('MANIM_OUTPUT_DIR', './media'))

        # Create a filename for the transparent PNG
        png_path = output_dir / 'images' / 'phase_encoding_final_frame.png'

        # Ensure the directory exists
        png_path.parent.mkdir(parents=True, exist_ok=True)

        # In newer Manim versions, we need to capture the frame differently
        frame = self.renderer.get_frame()

        # Convert to PIL Image and save as PNG
        image = Image.fromarray(frame)
        image.save(png_path, format='PNG')

        print(f"Final frame saved as: {png_path}")


class PhiDefinition(Scene):
    def construct(self):
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        phi_derivative = MathTex(
            r"\frac{d "
            r"\phi"
            r"}{d t} = \omega"
        ).scale(2)
        phi_derivative.set_color_by_tex(r"\phi", PINK)

        phi_integral = MathTex(
            r"\phi",
            r" = \int \omega \,dt"
        ).scale(2)
        phi_integral.set_color_by_tex(r"\phi", PINK)

        phi_derivative.next_to(ORIGIN, UP, buff=1)
        phi_integral.next_to(ORIGIN, DOWN, buff=1)
        self.add(phi_derivative, phi_integral)


class OmegaRelations(Scene):
    def construct(self):
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        omega_relations = MathTex(
            r"\omega",
            r" = \gamma",
            r"B(x, y)"
        ).scale(2)
        omega_relations[2].set_color(LIGHT_BLUE)

        self.play(Write(omega_relations))
        self.wait(4)

        omega_relations_2 = MathTex(
            r"\omega",
            r" = \gamma (",
            r"G_x x",
            r"+",
            r"G_y y",
            r")"
        ).scale(2)
        omega_relations_2[2].set_color(LIGHT_BLUE)
        omega_relations_2[4].set_color(LIGHT_GREEN)

        self.play(TransformMatchingTex(omega_relations, omega_relations_2))
        self.wait(4)


class FinalPhi(Scene):
    def construct(self):
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        phi_final = MathTex(
            r"\phi",
            r" = \gamma (",
            r"x\int G_x \,dt",
            r"+",
            r"y\int G_y \,dt",
            r")"
        ).scale(2)
        phi_final[0].set_color(PINK)
        phi_final[2].set_color(LIGHT_BLUE)
        phi_final[4].set_color(LIGHT_GREEN)

        self.play(Write(phi_final), run_time=4)
        self.wait(4)


class TotalSignalEquation(Scene):
    def construct(self):
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        equation = MathTex(
            r"s(t) = ",
            r"\int \int",
            r"M(x, y)",
            r"e^{i \gamma",
            r"x",
            r"\int G_x \,dt}",
            r"e^{i \gamma",
            r"y",
            r"\int G_y \,dt}",
            r" \,dx \,dy"
        ).scale(1.5)

        equation[2].set_color(LIGHT_GREEN)
        equation[4].set_color(LIGHT_BLUE)
        equation[7].set_color(PINK)

        self.add(equation)


class ImageToKSpace(Scene):
    def construct(self):
        # Set wider frame for better spacing
        self.camera.frame_width = 20
        self.camera.frame_height = 12

        # Load the brain image (make sure this path is correct)
        brain_img = ImageMobject("assets/brain-axial.png").scale(1.15)
        brain_img.rotate(90 * DEGREES)

        # Ensure the k-space image is properly created
        k_space_img = ImageMobject("assets/spectrum.png").scale(1.15)

        # Position the images with more separation (left and right sides)
        image_title = Text("Image Space", color=PINK).scale(0.8)
        k_space_title = Text("K-Space", color=PINK).scale(0.8)

        # Position far left and far right
        image_title.move_to(LEFT * 5.2 + UP * 4)
        k_space_title.move_to(RIGHT * 5.2 + UP * 4)

        brain_img.next_to(image_title, DOWN, buff=0.8)

        k_space_img.next_to(k_space_title, DOWN, buff=0.8)

        # Create FOV box in image space
        image_rect = Rectangle(
            width=brain_img.width,
            height=brain_img.height,
            color=LIGHT_BLUE,
            stroke_width=8
        ).move_to(brain_img)

        fov_label = Text("FOV", color=LIGHT_BLUE).scale(0.6)
        fov_label.next_to(image_rect, LEFT, buff=0.3)

        # Resolution indicators in image space
        delta_x_arrow = Arrow(
            start=brain_img.get_bottom() + LEFT * brain_img.width / 4,
            end=brain_img.get_bottom() + LEFT * brain_img.width / 4 + RIGHT * 0.5,
            color=LIGHT_GREEN,
            stroke_width=12,
            buff=0
        )
        delta_x_label = Text("Δx", color=LIGHT_GREEN).scale(0.5)
        delta_x_label.next_to(delta_x_arrow, DOWN, buff=0.2)

        # Nyquist limit in k-space
        k_space_rect = Rectangle(
            width=k_space_img.width,
            height=k_space_img.height,
            color=LIGHT_GREEN,
            stroke_width=8
        ).move_to(k_space_img)

        nyquist_label = Text("Nyquist", color=LIGHT_GREEN).scale(0.6)
        nyquist_label.next_to(k_space_rect, RIGHT, buff=0.3)

        # k-space resolution
        delta_k_arrow = Arrow(
            start=k_space_img.get_bottom() + RIGHT * k_space_img.width / 4,
            end=k_space_img.get_bottom() + RIGHT * k_space_img.width / 4 + LEFT * 0.5,
            color=LIGHT_BLUE,
            stroke_width=12,
            buff=0
        )
        delta_k_label = Text("Δkx", color=LIGHT_BLUE).scale(0.5)
        delta_k_label.next_to(delta_k_arrow, DOWN, buff=0.2)

        # Add relationship formulas - positioned at the center
        relationship1 = MathTex(r"\Delta k_x = \frac{1}{FOV_x}", color=LIGHT_BLUE).scale(0.8)
        relationship2 = MathTex(r"FOV_x = \frac{1}{\Delta k_x}", color=LIGHT_BLUE).scale(0.8)
        relationship3 = MathTex(r"\Delta x = \frac{1}{2k_{x,Nyquist}}", color=LIGHT_GREEN).scale(0.8)
        relationship4 = MathTex(r"k_{x,Nyquist} = \frac{1}{2\Delta x}", color=LIGHT_GREEN).scale(0.8)

        formulas = VGroup(relationship1, relationship2, relationship3, relationship4).arrange(DOWN, buff=0.3)
        formulas.move_to(ORIGIN)  # Center position

        # Animation sequence with longer pauses
        self.play(
            FadeIn(image_title),
            FadeIn(brain_img),
            run_time=1.5
        )
        self.wait(0.5)

        self.play(
            Create(image_rect)
        )

        self.play(
            Write(fov_label)
        )
        self.wait(1)  # Pause to process

        self.play(
            GrowArrow(delta_x_arrow),
        )

        self.play(
            Write(delta_x_label)
        )
        self.wait(1.5)  # Longer pause

        # Show k-space title first
        self.play(
            FadeIn(k_space_title),
            run_time=0.5
        )
        self.wait(0.5)

        # Show the transformation effect
        brain_copy = brain_img.copy()

        # Flash effect during transition
        flash = Flash(
            brain_copy,
            line_length=0.3,
            num_lines=30,
            color=WHITE,
            flash_radius=brain_img.width / 2,
            time_width=0.5
        )

        self.play(flash, run_time=1.5)
        self.wait(0.5)  # Pause after flash

        # Make sure k-space image appears properly
        self.play(
            FadeIn(k_space_img),
            run_time=1
        )
        self.wait(0.5)

        self.play(
            Create(k_space_rect),
            Write(nyquist_label)
        )
        self.wait(0.5)

        self.play(
            GrowArrow(delta_k_arrow)
        )

        self.play(
            Write(delta_k_label),
            run_time=1
        )
        self.wait(1.5)

        # Connect the relationships with arrows
        arrow1 = Arrow(
            start=fov_label.get_right() + RIGHT * 0.1,
            end=delta_k_label.get_left() + LEFT * 0.1,
            color=LIGHT_BLUE,
            buff=0.1
        )

        arrow2 = Arrow(
            start=delta_x_label.get_right() + RIGHT * 0.1,
            end=nyquist_label.get_bottom() + DOWN * 0.1,
            color=LIGHT_GREEN,
            buff=0.1
        )

        # Create curved arrows to avoid overlap
        path1 = CubicBezier(
            start_anchor=fov_label.get_right(),
            start_handle=fov_label.get_right() + RIGHT * 3 + UP * 2,
            end_handle=delta_k_label.get_left() + LEFT * 3 + UP * 2,
            end_anchor=delta_k_label.get_left(),
        )

        path2 = CubicBezier(
            start_anchor=delta_x_label.get_right(),
            start_handle=delta_x_label.get_right() + RIGHT * 3 + DOWN * 2,
            end_handle=nyquist_label.get_left() + LEFT * 3 + DOWN * 2,
            end_anchor=nyquist_label.get_left(),
        )

        curved_arrow1 = CurvedArrow(
            fov_label.get_right(),
            delta_k_label.get_left(),
            color=LIGHT_BLUE
        )

        curved_arrow2 = CurvedArrow(
            delta_x_label.get_right(),
            nyquist_label.get_left(),
            color=LIGHT_GREEN
        )

        # Play the arrow animations
        self.play(Create(curved_arrow1), run_time=1.5)
        self.play(Create(curved_arrow2), run_time=1.5)

        # Show the mathematical relationships
        self.play(Write(formulas), run_time=2)
        self.wait(3)  # Extended final pause


class KSpaceRelations(Scene):
    def construct(self):
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        # 3 equations
        # 1. resolution in image space maps to Nyquist rates
        # 2. FOV maps to resolution in k space
        # 3. both spaces have the same number of points

        nyquist_equation = MathTex(
            r"\Delta x = \frac{1}{2k_{x,Nyquist}}",
            color=LIGHT_GREEN
        )

        FOV_equation = MathTex(
            r"FOV_y = \frac{1}{\Delta k_y}",
            color=LIGHT_BLUE
        )

        num_points_equation = MathTex(
            r"N_{points, Image Space} = N_{points, KSpace}",
            color=PINK
        )

        # Scale and position the equations
        nyquist_equation.scale(1.5)
        FOV_equation.scale(1.5)
        num_points_equation.scale(1.5)

        nyquist_equation.move_to(UP * 2)
        FOV_equation.move_to(ORIGIN)
        num_points_equation.move_to(DOWN * 2)

        self.add(nyquist_equation, FOV_equation, num_points_equation)


class GRESequence(Scene):
    def construct(self):
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        # Create the 4 axes
        axes_width = 12
        axes_height = 1.5
        axes_spacing = 0.75

        # Create the axes
        slice_select_axes = self.create_labeled_axes("G_z", axes_width, axes_height, color=LIGHT_GREEN,
                                                     secondary_label="Slice Selection")
        rf_axes = self.create_labeled_axes("RF", axes_width, axes_height, color=BLACK)
        phase_encode_axes = self.create_labeled_axes("G_y", axes_width, axes_height, color=PINK,
                                                     secondary_label="Phase Encoding")
        freq_encode_axes = self.create_labeled_axes("G_x", axes_width, axes_height, color=LIGHT_BLUE,
                                                    secondary_label="Frequency Encoding")

        # Stack them vertically with proper alignment
        axes_group = VGroup(slice_select_axes, rf_axes, phase_encode_axes, freq_encode_axes)

        # Align all axes to the right edge of their labels
        for i in range(1, len(axes_group)):
            axes_group[i][0].align_to(axes_group[0][0], RIGHT)

        # Now arrange them vertically with proper spacing
        axes_group.arrange(DOWN, buff=axes_spacing, aligned_edge=RIGHT)

        # Ensure the actual axes (not the labels) are aligned
        for i in range(1, len(axes_group)):
            axes_group[i][0].align_to(axes_group[0][0], RIGHT)

        self.add(axes_group)

        # Timing parameters
        total_duration = 10  # in seconds
        ss_start = 1  # slice selection start
        ss_duration = 2  # slice selection duration
        ss_end = ss_start + ss_duration

        ss_rephase_start = ss_end
        ss_rephase_duration = 1
        ss_rephase_end = ss_rephase_start + ss_rephase_duration

        rf_start = ss_start
        rf_duration = ss_duration
        rf_end = rf_start + rf_duration
        rf_center = rf_start + rf_duration / 2

        pe_start = ss_rephase_end + 0.25
        pe_duration = 1.75  # phase encoding duration
        pe_end = pe_start + pe_duration

        fenc_rephase_start = pe_start
        fenc_rephase_duration = pe_duration
        fenc_rephase_end = fenc_rephase_start + fenc_rephase_duration

        fenc_readout_start = fenc_rephase_end
        fenc_readout_duration = 3
        fenc_readout_end = fenc_readout_start + fenc_readout_duration
        fenc_readout_center = fenc_readout_start + fenc_readout_duration / 2

        # Time markers
        time_markers = self.create_vertical_time_markers(
            [ss_start, ss_end, pe_start, pe_end, ss_rephase_end, fenc_readout_start, fenc_readout_end],
            [slice_select_axes, freq_encode_axes])

        # Create gradients and RF pulse
        ss_gradient = self.create_gradient_rectangle(slice_select_axes, ss_start, ss_duration, 1, color=LIGHT_GREEN)
        ss_rephase_gradient = self.create_gradient_rectangle(slice_select_axes, ss_rephase_start, ss_rephase_duration, -1, color=LIGHT_GREEN)
        rf_pulse = self.create_rf_pulse(rf_axes, rf_start, rf_duration, 1)
        pe_gradient = self.create_gradient_rectangle(phase_encode_axes, pe_start, pe_duration, 1, color=PINK)
        fenc_rephase_gradient = self.create_gradient_rectangle(freq_encode_axes, fenc_rephase_start,
                                                               fenc_rephase_duration, -0.5, color=LIGHT_BLUE)
        fenc_readout_gradient = self.create_gradient_rectangle(freq_encode_axes, fenc_readout_start,
                                                               fenc_readout_duration, 1, color=LIGHT_BLUE)

        # Create readout window
        readout_window = self.create_readout_window(rf_axes, fenc_readout_start, fenc_readout_duration)

        # Create TE
        # Get the actual positions on the axes for the centers
        rf_center_point = rf_axes[0].c2p(rf_center, 0)
        readout_center_point = rf_axes[0].c2p(fenc_readout_center, 0)

        # Create a brace between these two points
        te_brace = BraceBetweenPoints(
            rf_center_point,
            readout_center_point,
            color=BLACK,
            direction=DOWN,
            buff=0.25
        )
        te_label = MathTex("T_E", color=BLACK).next_to(te_brace, DOWN, buff=0.1)

        # Animations
        # self.play(Create(VGroup(*time_markers)), run_time=1)
        self.add(*time_markers)

        # Slice selection and RF pulse
        # self.play(
        #     Create(ss_gradient),
        #     Create(rf_pulse),
        #     run_time=2
        # )
        self.add(ss_gradient, rf_pulse, ss_rephase_gradient)

        # Phase encoding and frequency encoding rephase
        # self.play(
        #     Create(pe_gradient),
        #     Create(fenc_rephase_gradient),
        #     Create(ss_rephase_gradient),
        #     run_time=1.5
        # )
        self.add(pe_gradient, fenc_rephase_gradient)

        # Frequency encoding readout
        # self.play(
        #     Create(fenc_readout_gradient),
        #     Create(readout_window),
        #     run_time=2
        # )
        self.add(fenc_readout_gradient, readout_window)

        # Show TE and TR
        # self.play(
        #     Create(te_brace),
        #     Create(te_label),
        #     run_time=1.5
        # )
        self.add(te_label, te_brace)

        # Show multiple phase encoding steps
        additional_pe_gradients = []
        num_additional_steps = 5
        for i in range(1, num_additional_steps + 1):
            # Calculate gradient amplitude as a fraction of the original
            # Alternate between positive and negative values
            if i % 2 == 0:
                amplitude = 1 - (i / num_additional_steps)
            else:
                amplitude = -(i / num_additional_steps)

            pe_grad = self.create_gradient_rectangle(
                phase_encode_axes,
                pe_start,
                pe_duration,
                amplitude,
                color=PINK,
                fill_opacity=0.3
            )
            additional_pe_gradients.append(pe_grad)

        # self.play(
        #     *[Create(grad) for grad in additional_pe_gradients],
        #     run_time=2
        # )
        self.add(*[grad for grad in additional_pe_gradients])

        # self.wait(1)

    def create_labeled_axes(self, label, width, height, color=WHITE, secondary_label=None):
        # Create axes with label but without y-axis
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1, 1, 0.5],
            x_length=width,
            y_length=height,
            axis_config={"include_tip": False, "include_numbers": False, "color": BLACK},
            y_axis_config={"include_ticks": False, "stroke_opacity": 0}  # Hide y-axis
        )

        labels = VGroup()

        label_tex = MathTex(label, color=color)
        labels.add(label_tex)

        if secondary_label:
            secondary_label_tex = Tex(secondary_label, color=color).scale(0.5)
            secondary_label_tex.next_to(label_tex, DOWN, buff=0.3)
            labels.add(secondary_label_tex)

        labels.next_to(axes.y_axis, LEFT, buff=0.2)
        return VGroup(axes, labels)

    def create_vertical_time_markers(self, time_points, connecting_axes):
        markers = []

        # Get the top and bottom y coordinates for our dashed lines
        top_y = connecting_axes[0][0].get_origin()[1] + connecting_axes[0][0].get_y_axis().get_height() / 2
        bottom_y = connecting_axes[-1][0].get_origin()[1] - connecting_axes[-1][0].get_y_axis().get_height() / 2

        for time in time_points:
            # Get the x coordinate for this time point
            x = connecting_axes[0][0].c2p(time, 0)[0]

            # Create dashed line
            line = DashedLine(
                start=[x, top_y, 0],
                end=[x, bottom_y, 0],
                stroke_width=1,
                color=BLACK,
                dash_length=0.1
            )
            markers.append(line)

        return markers

    def create_gradient_rectangle(self, axes, start_time, duration, amplitude, color=WHITE, fill_opacity=1):
        # Calculate coordinates in axes space
        x_start = start_time
        x_end = start_time + duration
        y_height = amplitude

        # Convert to pixel coordinates
        p1 = axes[0].c2p(x_start, 0)
        p2 = axes[0].c2p(x_end, y_height)

        # Create the rectangle
        rect = Rectangle(
            width=p2[0] - p1[0],
            height=abs(p2[1] - p1[1]),
            stroke_width=1.5,
            fill_color=color,
            fill_opacity=fill_opacity,
            color=BLACK
        )

        # rect.points_in_order = [
        #     [p1[0], p1[1], 0],  # bottom left
        #     [p1[0], p1[1] + abs(p2[1] - p1[1]), 0],  # top left
        #     [p2[0], p2[1], 0],  # top right
        #     [p2[0], p1[1], 0]  # bottom right
        # ]

        # Position the rectangle
        rect.move_to((p1 + p2) / 2)

        return rect

    def create_rf_pulse(self, rf_axes, start_time, duration, amplitude):
        # Create a sinc pulse for RF
        axes = rf_axes[0]
        center = start_time + duration / 2
        width = duration * 0.8

        x_values = np.linspace(start_time, start_time + duration, 100)

        # Calculate sinc values with some adjustments to fit in the window
        # Create a sinc function that's 0 at the start and end of the window
        x_norm = (x_values - center) / (width / 5)
        y_values = amplitude * np.sinc(x_norm)

        # Create points for the curve
        points = [axes.c2p(x, y) for x, y in zip(x_values, y_values)]

        # Create the curve
        rf_pulse = VMobject()
        rf_pulse.set_points_smoothly(points)
        rf_pulse.set_stroke(YELLOW, width=2)

        return rf_pulse

    def create_readout_window(self, rf_axes, start_time, duration):
        # Create a box to indicate the readout window
        axes = rf_axes[0]

        # Calculate coordinates
        p1 = axes.c2p(start_time, -0.8)
        p2 = axes.c2p(start_time + duration, 0.8)

        # Create the rectangle
        rect = Rectangle(
            width=p2[0] - p1[0],
            height=p2[1] - p1[1],
            stroke_width=1.5,
            stroke_color=YELLOW,
            fill_opacity=1,
            fill_color=YELLOW
        )

        read_out_label = Tex("Readout Window", color=BLACK).scale(0.5)

        # Position the rectangle
        rect.move_to((p1 + p2) / 2)
        read_out_label.move_to(rect.get_center())

        return VGroup(rect, read_out_label)

    def create_time_brace(self, start_time, end_time, label_text, direction):
        # Create a brace to indicate TE or TR times

        # Calculate midpoint y position for the brace
        midpoint_y = 0

        # Calculate the start and end points
        start_point = np.array([start_time, midpoint_y, 0])
        end_point = np.array([end_time, midpoint_y, 0])

        # Create the brace
        brace = BraceBetweenPoints(
            start_point,
            end_point,
            direction=direction,
            buff=0.5
        )

        # Add the label
        label = MathTex(label_text)
        label.next_to(brace, direction, buff=0.1)

        return VGroup(brace, label)


class KSpaceTraversal(Scene):
    def construct(self):
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        # Create the 4 axes
        axes_width = 12
        axes_height = 1.5
        axes_spacing = 0.75

        # Create the gradient axes
        gx_axes = self.create_labeled_axes("G_x", axes_width, axes_height, color=LIGHT_BLUE,
                                           secondary_label="Frequency Encoding")
        gy_axes = self.create_labeled_axes("G_y", axes_width, axes_height, color=PINK,
                                           secondary_label="Phase Encoding")

        # Create the k-space axes
        kx_axes = self.create_labeled_axes("k_x", axes_width, axes_height, color=LIGHT_BLUE)
        ky_axes = self.create_labeled_axes("k_y", axes_width, axes_height, color=PINK)

        # Stack them vertically with proper alignment
        axes_group = VGroup(gx_axes, gy_axes, kx_axes, ky_axes)

        # Align all axes to the right edge of their labels
        for i in range(1, len(axes_group)):
            axes_group[i][0].align_to(axes_group[0][0], RIGHT)

        # Now arrange them vertically with proper spacing
        axes_group.arrange(DOWN, buff=axes_spacing, aligned_edge=RIGHT)

        # Ensure the actual axes (not the labels) are aligned
        for i in range(1, len(axes_group)):
            axes_group[i][0].align_to(axes_group[0][0], RIGHT)

        self.add(axes_group)

        # Timing parameters
        total_duration = 10  # in seconds

        # Phase encoding
        pe_start = 1
        pe_duration = 1.75
        pe_end = pe_start + pe_duration

        # Frequency encoding rephase
        fenc_rephase_start = pe_start
        fenc_rephase_duration = pe_duration
        fenc_rephase_end = fenc_rephase_start + fenc_rephase_duration

        # Frequency encoding readout
        fenc_readout_start = fenc_rephase_end
        fenc_readout_duration = 3
        fenc_readout_end = fenc_readout_start + fenc_readout_duration

        # Time markers
        time_markers = self.create_vertical_time_markers(
            [pe_start, pe_end, fenc_readout_start, fenc_readout_end],
            [gx_axes, ky_axes])

        # self.play(Create(VGroup(*time_markers)), run_time=1)
        self.add(*time_markers)

        # Create gradients for G_x and G_y
        pe_gradient = self.create_gradient_rectangle(gy_axes, pe_start, pe_duration, 1, color=PINK)
        fenc_rephase_gradient = self.create_gradient_rectangle(gx_axes, fenc_rephase_start,
                                                               fenc_rephase_duration, -0.5, color=LIGHT_BLUE)

        # Play the phase encoding and frequency rephasing gradients animation
        # self.play(
        #     Create(pe_gradient),
        #     Create(fenc_rephase_gradient),
        #     run_time=1.5
        # )
        self.add(pe_gradient, fenc_rephase_gradient)

        # Create k-space changes from phase encoding and frequency rephase
        # For k_y: Integral of G_y creates a step function
        ky_change_points = [
            ky_axes[0].c2p(pe_start, 0),
            ky_axes[0].c2p(pe_end, 1)  # Step up to final value
        ]

        ky_change = VMobject()
        ky_change.set_points_as_corners(ky_change_points)
        ky_change.set_stroke(PINK, width=2)

        # For k_x: Integral of G_x creates negative ramp during rephase
        kx_rephase_points = [
            kx_axes[0].c2p(fenc_rephase_start, 0),
            kx_axes[0].c2p(fenc_rephase_end, -1)  # Ramp down to negative value
        ]

        kx_rephase = VMobject()
        kx_rephase.set_points_as_corners(kx_rephase_points)
        kx_rephase.set_stroke(LIGHT_BLUE, width=2)

        # Play k-space changes for phase encoding and frequency rephase
        # self.play(
        #     Create(ky_change),
        #     Create(kx_rephase),
        #     run_time=1.5
        # )
        self.add(ky_change, kx_rephase)

        # Create frequency readout gradient
        fenc_readout_gradient = self.create_gradient_rectangle(gx_axes, fenc_readout_start,
                                                               fenc_readout_duration, 1, color=LIGHT_BLUE)

        # Play frequency readout gradient animation
        # self.play(
        #     Create(fenc_readout_gradient),
        #     run_time=1.5
        # )
        self.add(fenc_readout_gradient)

        # Create k_x change during readout (from negative to positive)
        kx_readout_points = [
            kx_axes[0].c2p(fenc_readout_start, -1),  # Start from negative value
            kx_axes[0].c2p(fenc_readout_end, 1)  # Ramp up to positive value
        ]

        ky_readout_points = [
            ky_axes[0].c2p(pe_end, 1),  # Maintain value
            ky_axes[0].c2p(fenc_readout_end, 1)  # Maintain value
        ]

        kx_readout = VMobject()
        kx_readout.set_points_as_corners(kx_readout_points)
        kx_readout.set_stroke(LIGHT_BLUE, width=2)

        ky_readout = VMobject()
        ky_readout.set_points_as_corners(ky_readout_points)
        ky_readout.set_stroke(PINK, width=2)

        # Play k_x change during readout
        # self.play(
        #     Create(kx_readout),
        #     Create(ky_readout),
        #     run_time=1.5
        # )
        self.add(kx_readout, ky_readout)

        # self.wait(1)

        # Now show another phase encoding path
        pe_gradients = []
        amplitudes = [0.5, 0, -0.5, -1]
        for amp in amplitudes:
            pe_grad = self.create_gradient_rectangle(gy_axes, pe_start, pe_duration, amp, color=PINK,
                                                     fill_opacity=0.3)
            pe_gradients.append(pe_grad)

        self.add(*pe_gradients)

        # Create k_y change for the new phase encoding
        all_ky_changes = []
        for amp in amplitudes:
            ky_change_points = [
                ky_axes[0].c2p(pe_start, 0),
                ky_axes[0].c2p(pe_end, amp),  # Step up to the new value
                ky_axes[0].c2p(fenc_readout_end, amp)  # Maintain value
            ]

            ky_change = VMobject()
            ky_change.set_points_as_corners(ky_change_points)
            ky_change.set_stroke(PINK, width=2, opacity=0.8)

            all_ky_changes.append(ky_change)

        self.add(*all_ky_changes)

        # Highlight the new k-space trajectory
        # self.play(
        #     ky_change2.animate.set_stroke(opacity=1, width=3),
        #     pe_gradient2.animate.set_opacity(1),
        #     run_time=1
        # )
        #
        # self.wait(2)

    def create_labeled_axes(self, label, width, height, color=WHITE, secondary_label=None):
        # Create axes with label but without y-axis
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1, 1, 0.5],
            x_length=width,
            y_length=height,
            axis_config={"include_tip": False, "include_numbers": False},
            y_axis_config={"include_ticks": False, "stroke_opacity": 0}  # Hide y-axis
        )

        labels = VGroup()

        label_tex = MathTex(label, color=color)
        labels.add(label_tex)

        if secondary_label:
            secondary_label_tex = Tex(secondary_label, color=color).scale(0.5)
            secondary_label_tex.next_to(label_tex, DOWN, buff=0.3)
            labels.add(secondary_label_tex)

        labels.next_to(axes.y_axis, LEFT, buff=0.2)
        return VGroup(axes, labels)

    def create_vertical_time_markers(self, time_points, connecting_axes):
        markers = []

        # Get the top and bottom y coordinates for our dashed lines
        top_y = connecting_axes[0][0].get_origin()[1] + connecting_axes[0][0].get_y_axis().get_height() / 2
        bottom_y = connecting_axes[-1][0].get_origin()[1] - connecting_axes[-1][0].get_y_axis().get_height() / 2

        for time in time_points:
            # Get the x coordinate for this time point
            x = connecting_axes[0][0].c2p(time, 0)[0]

            # Create dashed line
            line = DashedLine(
                start=[x, top_y, 0],
                end=[x, bottom_y, 0],
                stroke_width=1,
                dash_length=0.1
            )
            markers.append(line)

        return markers

    def create_gradient_rectangle(self, axes, start_time, duration, amplitude, color=WHITE, fill_opacity=1):
        # Calculate coordinates in axes space
        x_start = start_time
        x_end = start_time + duration
        y_height = amplitude

        # Convert to pixel coordinates
        p1 = axes[0].c2p(x_start, 0)
        p2 = axes[0].c2p(x_end, y_height)

        # Create the rectangle
        rect = Rectangle(
            width=p2[0] - p1[0],
            height=abs(p2[1] - p1[1]),
            stroke_width=1.5,
            fill_color=color,
            fill_opacity=fill_opacity
        )

        # Position the rectangle
        rect.move_to((p1 + p2) / 2)

        return rect


class EPISequenceTraversal(Scene):
    def construct(self):
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        # Create the 4 axes
        axes_width = 12
        axes_height = 1.5
        axes_spacing = 0.75

        # Create the gradient axes
        gx_axes = self.create_labeled_axes("G_x", axes_width, axes_height, color=LIGHT_BLUE,
                                           secondary_label="Frequency Encoding")
        gy_axes = self.create_labeled_axes("G_y", axes_width, axes_height, color=PINK,
                                           secondary_label="Phase Encoding")

        # Create the k-space axes
        kx_axes = self.create_labeled_axes("k_x", axes_width, axes_height, color=LIGHT_BLUE)
        ky_axes = self.create_labeled_axes("k_y", axes_width, axes_height, color=PINK)

        # Stack them vertically with proper alignment
        axes_group = VGroup(gx_axes, gy_axes, kx_axes, ky_axes)

        # Align all axes to the right edge of their labels
        for i in range(1, len(axes_group)):
            axes_group[i][0].align_to(axes_group[0][0], RIGHT)

        # Now arrange them vertically with proper spacing
        axes_group.arrange(DOWN, buff=axes_spacing, aligned_edge=RIGHT)

        # Ensure the actual axes (not the labels) are aligned
        for i in range(1, len(axes_group)):
            axes_group[i][0].align_to(axes_group[0][0], RIGHT)

        self.add(axes_group)

        # Timing parameters
        total_duration = 10  # in seconds

        # Phase encoding
        pe_start = 0
        pe_duration = 0.5
        pe_end = pe_start + pe_duration

        f_enc_duration = 1
        pulse_duration = 0.125
        pe_pulses = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]


        # Time markers
        time_markers = self.create_vertical_time_markers(
            pe_pulses,
            [gx_axes, ky_axes])

        # self.play(Create(VGroup(*time_markers)), run_time=1)
        self.add(*time_markers)

        # Create gradients for G_x and G_y
        pe_gradient = self.create_gradient_rectangle(gy_axes, pe_start, pe_duration, -1, color=PINK)
        fenc_rephase_gradient = self.create_gradient_rectangle(gx_axes, pe_start,
                                                               pe_duration, -1, color=LIGHT_BLUE)

        # Play the phase encoding and frequency rephasing gradients animation
        # self.play(
        #     Create(pe_gradient),
        #     Create(fenc_rephase_gradient),
        #     run_time=1.5
        # )
        self.add(pe_gradient, fenc_rephase_gradient)

        gx_gradients = []
        gy_pulses = []
        last_gx_direction = 1

        kx_phases = []
        ky_phases = []
        last_ky = -1

        for pulse in pe_pulses:
            # Create the G_x gradient
            gx_gradient = self.create_gradient_rectangle(gx_axes, pulse, f_enc_duration, 0.5 * last_gx_direction, color=LIGHT_BLUE)
            gx_gradients.append(gx_gradient)
            last_gx_direction *= -1

            kx_change_points = [
                kx_axes[0].c2p(pulse, last_gx_direction),
                kx_axes[0].c2p(pulse + f_enc_duration, -last_gx_direction)  # Step up to final value
            ]
            kx_change = VMobject()
            kx_change.set_points_as_corners(kx_change_points)
            kx_change.set_stroke(LIGHT_BLUE, width=2)
            kx_phases.append(kx_change)

            ky_change_points = [
                ky_axes[0].c2p(pulse, last_ky),
                ky_axes[0].c2p(pulse + f_enc_duration - pulse_duration / 2, last_ky),
                ky_axes[0].c2p(pulse + f_enc_duration, last_ky + 0.2)  # Step up to final value
            ]
            last_ky += 0.2

            ky_change = VMobject()
            ky_change.set_points_as_corners(ky_change_points)
            ky_change.set_stroke(PINK, width=2)
            ky_phases.append(ky_change)

            if pulse == 0.5:
                continue

            # Create the G_y pulse
            gy_pulse = self.create_gradient_rectangle(gy_axes, pulse - pulse_duration / 2, pulse_duration, 1, color=PINK)
            gy_pulses.append(gy_pulse)

        self.add(*gx_gradients, *gy_pulses)

        # Create k-space changes from phase encoding and frequency rephase
        # For k_y: Integral of G_y creates a step function
        ky_change_points = [
            ky_axes[0].c2p(pe_start, 0),
            ky_axes[0].c2p(pe_end, -1)  # Step up to final value
        ]

        ky_change = VMobject()
        ky_change.set_points_as_corners(ky_change_points)
        ky_change.set_stroke(PINK, width=2)

        # For k_x: Integral of G_x creates negative ramp during rephase
        kx_rephase_points = [
            kx_axes[0].c2p(pe_start, 0),
            kx_axes[0].c2p(pe_end, -1)  # Ramp down to negative value
        ]

        kx_rephase = VMobject()
        kx_rephase.set_points_as_corners(kx_rephase_points)
        kx_rephase.set_stroke(LIGHT_BLUE, width=2)

        # Play k-space changes for phase encoding and frequency rephase
        # self.play(
        #     Create(ky_change),
        #     Create(kx_rephase),
        #     run_time=1.5
        # )
        self.add(ky_change, kx_rephase)

        self.add(ky_phases[0], kx_phases[0])
        self.add(kx_phases[1])
        self.add(ky_phases[1])
        self.add(ky_phases[2], kx_phases[2])
        self.add(ky_phases[3], kx_phases[3])
        self.add(ky_phases[4], kx_phases[4])
        self.add(ky_phases[5], kx_phases[5])
        self.add(ky_phases[6], kx_phases[6])
        self.add(ky_phases[7], kx_phases[7])
        self.add(ky_phases[8], kx_phases[8])

        # Create frequency readout gradient
        # fenc_readout_gradient = self.create_gradient_rectangle(gx_axes, fenc_readout_start,
        #                                                        fenc_readout_duration, 1, color=LIGHT_BLUE)
        #
        # # Play frequency readout gradient animation
        # # self.play(
        # #     Create(fenc_readout_gradient),
        # #     run_time=1.5
        # # )
        # # self.add(fenc_readout_gradient)
        #
        # # Create k_x change during readout (from negative to positive)
        # kx_readout_points = [
        #     kx_axes[0].c2p(fenc_readout_start, -1),  # Start from negative value
        #     kx_axes[0].c2p(fenc_readout_end, 1)  # Ramp up to positive value
        # ]
        #
        # ky_readout_points = [
        #     ky_axes[0].c2p(pe_end, 1),  # Maintain value
        #     ky_axes[0].c2p(fenc_readout_end, 1)  # Maintain value
        # ]
        #
        # kx_readout = VMobject()
        # kx_readout.set_points_as_corners(kx_readout_points)
        # kx_readout.set_stroke(LIGHT_BLUE, width=2)
        #
        # ky_readout = VMobject()
        # ky_readout.set_points_as_corners(ky_readout_points)
        # ky_readout.set_stroke(PINK, width=2)

        # Play k_x change during readout
        # self.play(
        #     Create(kx_readout),
        #     Create(ky_readout),
        #     run_time=1.5
        # )
        # self.add(kx_readout, ky_readout)

    def create_labeled_axes(self, label, width, height, color=WHITE, secondary_label=None):
        # Create axes with label but without y-axis
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1, 1, 0.5],
            x_length=width,
            y_length=height,
            axis_config={"include_tip": False, "include_numbers": False},
            y_axis_config={"include_ticks": False, "stroke_opacity": 0}  # Hide y-axis
        )

        labels = VGroup()

        label_tex = MathTex(label, color=color)
        labels.add(label_tex)

        if secondary_label:
            secondary_label_tex = Tex(secondary_label, color=color).scale(0.5)
            secondary_label_tex.next_to(label_tex, DOWN, buff=0.3)
            labels.add(secondary_label_tex)

        labels.next_to(axes.y_axis, LEFT, buff=0.2)
        return VGroup(axes, labels)

    def create_vertical_time_markers(self, time_points, connecting_axes):
        markers = []

        # Get the top and bottom y coordinates for our dashed lines
        top_y = connecting_axes[0][0].get_origin()[1] + connecting_axes[0][0].get_y_axis().get_height() / 2
        bottom_y = connecting_axes[-1][0].get_origin()[1] - connecting_axes[-1][0].get_y_axis().get_height() / 2

        for time in time_points:
            # Get the x coordinate for this time point
            x = connecting_axes[0][0].c2p(time, 0)[0]

            # Create dashed line
            line = DashedLine(
                start=[x, top_y, 0],
                end=[x, bottom_y, 0],
                stroke_width=1,
                dash_length=0.1
            )
            markers.append(line)

        return markers

    def create_gradient_rectangle(self, axes, start_time, duration, amplitude, color=WHITE, fill_opacity=1):
        # Calculate coordinates in axes space
        x_start = start_time
        x_end = start_time + duration
        y_height = amplitude

        # Convert to pixel coordinates
        p1 = axes[0].c2p(x_start, 0)
        p2 = axes[0].c2p(x_end, y_height)

        # Create the rectangle
        rect = Rectangle(
            width=p2[0] - p1[0],
            height=abs(p2[1] - p1[1]),
            stroke_width=1.5,
            fill_color=color,
            fill_opacity=fill_opacity
        )

        # Position the rectangle
        rect.move_to((p1 + p2) / 2)

        return rect
