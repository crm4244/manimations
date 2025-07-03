from manim import *
from portal import *
# import numpy as np
from manim.typing import Vector3D


# this is going to be a longer animation showing how the C2Y portal is a quoitent portal of a standard 6-world triple portal


class TheC2YPortal(Scene):
    def construct(self):
        
        portal = StarPortal(3, [lambda x: x], [[0]], star_center=3*UP, segment_length=2, angle=PI/2)
        self.add(portal)

        colors = [PURE_BLUE, PURE_GREEN, PURE_RED]
        nodes = self.get_colored_regions(portal, colors)
        self.add(nodes)
        
        self.wait(1)
        self.play(*[ReplacementTransform(r, Dot(r.get_center_of_mass(), radius=0.3).match_style(r).set_opacity(1)) for r in nodes])
        self.play(nodes.animate.rotate(-PI/3).move_to(2.5*DOWN))
        # self.play(nodes.animate.arrange(RIGHT).move_to(nodes.get_center_of_mass()))

        full = nodes[0]
        half1, half2 = self.split_circle(full, PI/2)
        nodes[0] = half1
        nodes.add(half2)

        self.play(VGroup(half1, half2).move_to(full.get_center()).animate.arrange(RIGHT).move_to(full.get_center()))
        
        nodes_copy = nodes.copy()
        nodes_copy[0].rotate(PI)
        nodes_copy[-1].rotate(PI)
        nodes_copy.arrange(RIGHT).move_to(nodes_copy.get_center())

        anims = []
        for i, node_copy in enumerate(nodes_copy):
            node = nodes[i]
            anim = node.animate.move_to(node_copy.get_center())
            if i == 0 or i == len(nodes)-1:
                anim.rotate(PI)
            anims.append(anim)

        
        self.play(*anims)
        # self.play(Transform(node_copy, nodes_copy))


    def get_colored_regions(self, portal: Portal, colors: list[ParsableManimColor]) -> VGroup:
        colored_regions = VGroup()
        regions = [r for w in portal.regions_by_world for r in w]
        if len(colors) < len(regions): raise Exception("Not enough colors!!! Need more color!!!")

        for i in range(len(regions)):
            region_copy = regions[i].copy().clear_updaters()
            region_copy.scale(0.9, about_point=portal.star_center)
            region_copy.set_fill(colors[i], opacity=0.3)
            colored_regions.add(region_copy)
        
        return colored_regions


    def split_circle(self, circle: Circle, split_angle: float) -> tuple[Sector, Sector]:
        first_half = Sector(
            radius=circle.radius,
            angle=PI,
            start_angle=split_angle,
            arc_center=circle.arc_center
        ).match_style(circle)
        
        second_half = first_half.copy().rotate(PI, about_point=circle.arc_center)
        return (first_half, second_half)



