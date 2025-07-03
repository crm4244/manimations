from manim import *
from portal import StarPortal


class C2YPatternedColorDots(Scene):
    def construct(self):
        

        size = 1

        # funcs = [(lambda x, i=i: x + 2*size * RIGHT * (i-(6-1)/2)) for i in range(6)]
        funcs = [(lambda x, i=i: x + rotate_vector(2.5 * RIGHT, i * TAU/6)) for i in range(6)]
        
        
        gluing_pattern = [[0, 2, 1], [1, 5, 3], [2, 4, 5], [3, 1, 0], [4, 0, 2], [5, 3, 4]]
        portal = StarPortal(3, funcs, gluing_pattern, segment_length=size, angle=PI/2)
        self.add(portal)

        colors = [PURE_RED, ORANGE, YELLOW, PURE_GREEN, PURE_BLUE, PINK]
        dots = VGroup()
        for i in range(6):
            dot = Dot(rotate_vector(size/2 * RIGHT, PI * 5/6), color=colors[i])
            dots.add(dot)
            portal.restrict(dot, world_index=i, region_index=0)
        self.add(dots)

        self.play(Rotate(dots, angle=TAU, about_point=ORIGIN), run_time=5, rate_func=linear)
