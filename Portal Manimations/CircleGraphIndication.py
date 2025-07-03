from manim import *
from typing import Any


class CircleGraphIndication(Scene):
    def construct(self):
        
        def how_close(parameter: ValueTracker, index: int, num_nodes: int, rate_func) -> float:
            center = float(index) / num_nodes
            actual_value = parameter.get_value()

            distance = abs(actual_value - center)
            if distance > 0.5:
                distance = 1 - distance
            
            return 1 - rate_func(distance * num_nodes)
        
        n = 6
        alpha = ValueTracker(0)
        self.add(alpha)

        dependent_values = []
        for i in range(n-1):
            v = ValueTracker()
            v.index = i
            v.add_updater(lambda x:
                x.set_value(how_close(alpha, x.index, n-1, smoothererstep))
            )

            self.add(v)
            dependent_values.append(v)

            
        circles_radius = 0.5
        circles = []
        circles_group = Group()
        for i in range(n):

            def update_circle(x):
                new_x = Circle(radius=circles_radius * (1 + x.value_tracker.get_value()))
                new_x.move_to(x)
                new_x.match_style(x)
                x.become(new_x)
            
            new_circle = Circle(radius=circles_radius)
            new_circle.value_tracker = dependent_values[i % (n-1)]
            new_circle.add_updater(update_circle)

            circles.append(new_circle)
            circles_group.add(new_circle)
        
        circles_group.arrange(RIGHT, 1)
        self.add(circles_group)

        for i in range(n-1):
            line = LineConnector(circles[i], circles[i+1], color=BLUE)
            self.add(line)

        dot = Dot().shift(UP * 1.5).add_updater(lambda x:
            x.set_x(interpolate(circles[0].get_x(), circles[n-1].get_x(), alpha.get_value()))
        )
        self.add(dot)

        self.play(alpha.animate.set_value(1), run_time=5, rate_func=smoothererstep)
        





class LineConnector(Line):
    def __init__(
        self,
        start_mobject: Mobject,
        end_mobject: Mobject,
        do_update: bool = True,
        **kwargs: Any,
    ) -> None:
        self.start_mobject = start_mobject
        self.end_mobject = end_mobject
        super().__init__(**kwargs)
        if (do_update):
            self.add_updater(lambda x:
                x.set_points_by_ends(self.start_mobject, self.end_mobject)
            )