from manim import *
from portal import StarPortal



class StarPortalExample(Scene):
    def construct(self):
        
        n=5
        p=2
        size = 3.6
        
        center = LEFT*4 # for testing
        funcs = [(lambda x, i=i: rotate_vector(x-center, (n+1-p)*i*TAU/n)+center) for i in range(n)]
        gluing_pattern = [[(j+i)%n for i in range(n)] for j in range(n)]
        portal = StarPortal(
            n,
            funcs,
            gluing_pattern,
            star_center = center,
            segment_length = size,
            angle = PI/2
        )
        self.add(portal)

        sq = Square(side_length=0.9, color=RED).shift(2*RIGHT - center)
        portal.restrict(sq, 0, 0)
        
        self.play(MoveAlongPath(sq, Circle().shift(center)), run_time=5, rate_func=smooth)
        self.play(sq.animate.scale(2))
        self.play(sq.animate.shift(LEFT))
        self.play(Rotating(sq))
        self.play(sq.animate.shift(RIGHT))
        self.play(sq.animate.scale(1/2))