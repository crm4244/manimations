from manim import *
from manim.typing import (
    Point3D,
    Point3DLike,
    MappingFunction,
)

__all__ = ["Portal", "StarPortal"]



class Portal(VMobject):
    def __init__(
        self,
        surface: VMobject,
        regions: list[VMobject],
        portal_functions: list[MappingFunction],
        gluing_pattern: list[list[int]],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.gluing_pattern = gluing_pattern
        self.portal_functions = portal_functions
        

        self.worlds: list[VGroup] = []
        self.surfaces: list[VMobject] = []
        self.regions_by_world: list[list[VMobject]] = []
        self.tracked_mobjects: dict[VMobject, list[VMobject]] = {}

        self.num_worlds = len(self.portal_functions)
        for world_index in range(self.num_worlds):

            surface_copy = self.get_portaled_vmobject(surface, world_index)
            surface_copy.set_z_index(self.z_index + 1)
            self.surfaces.append(surface_copy)
            
            world = VGroup(surface_copy)
            self.worlds.append(world)

            region_copies = []
            for region in regions:
                region_copy = self.get_portaled_vmobject(region, world_index, hidden=True)
                region_copies.append(region_copy)
                world.add(region_copy)
            self.regions_by_world.append(region_copies)
            self.add(world)
            
    
    def restrict_by_key(self, vmobject: VMobject, gluing_key: int) -> None:
        vmobject.style_saved_by_portal = vmobject.copy()
        vmobject.set_opacity(0)

        restricted_copies = []
        for other_world_index in range(self.num_worlds):
            
            other_world_gluing_pattern = self.gluing_pattern[other_world_index]
            for i, other_key in enumerate(other_world_gluing_pattern):
                if gluing_key == other_key:

                    restriction_region = self.regions_by_world[other_world_index][i]
                    restricted_copy = self.get_portaled_vmobject(vmobject, world_index=other_world_index, restriction_region=restriction_region)
                    
                    restricted_copies.append(restricted_copy)
                    self.worlds[other_world_index].add(restricted_copy)
                
        self.tracked_mobjects[vmobject] = restricted_copies
    

    def restrict(self, vmobject: VMobject, world_index: int, region_index: int) -> None:
        gluing_key = self.gluing_pattern[world_index][region_index]
        self.restrict_by_key(vmobject, gluing_key)


    def free(self, vmobject: VMobject, world_index: int) -> None:
        vmobject.match_style(vmobject.style_saved_by_portal)
        vmobject.apply_function(self.portal_functions[world_index])

        for vmobject_copy in self.tracked_mobjects[vmobject]:
            self.worlds[vmobject_copy._world_index].remove(vmobject_copy)


    def get_portaled_vmobject(self, vmobject: VMobject, world_index: int, hidden: bool = False, restriction_region: VMobject = None) -> VMobject:
        restricted = restriction_region is not None

        def update_portaled_vmobject(x: VMobject) -> VMobject:
            portaled_original = x._original.copy()
            portaled_original.apply_function(x._func)
            
            if (x._restricted):
                inter = Intersection(portaled_original, x._restriction_region)
                inter.match_style(x._original.style_saved_by_portal)
                x.become(inter)
            else:
                x.become(portaled_original)
            
            if x._hidden:
                x.set_opacity(0)
            
            return x

        portaled_vmobject = VMobject() if restricted else vmobject.copy()
        portaled_vmobject._original = vmobject
        portaled_vmobject._world_index = world_index
        portaled_vmobject._hidden = hidden
        portaled_vmobject._func = self.portal_functions[world_index]
        portaled_vmobject._restricted = restricted
        portaled_vmobject._restriction_region = restriction_region
        portaled_vmobject.add_updater(update_portaled_vmobject)

        update_portaled_vmobject(portaled_vmobject)
        return portaled_vmobject






class StarPortal(Portal):
    def __init__(
        self,
        n: int,
        portal_functions: list[MappingFunction],
        gluing_pattern: list[list[int]],
        color: ParsableManimColor = WHITE,
        star_center: Point3DLike = ORIGIN,
        segment_length: float = 1,
        angle: float = 0,
        **kwargs,
    ) -> None:
        self.n = n
        self.star_center = star_center
        
        self.main_surface = VGroup()
        regions = []
        for i in range(n):
            segment = Line(ORIGIN, RIGHT * segment_length, color=color)
            segment.rotate_about_origin(angle + TAU*i/self.n)
            segment.shift(star_center)
            self.main_surface.add(segment)

            sector = Sector(radius=segment_length, angle=TAU / n, start_angle=angle)
            sector.rotate_about_origin(TAU*i/self.n)
            sector.shift(star_center)
            regions.append(sector)
        
        super().__init__(self.main_surface, regions, portal_functions, gluing_pattern, **kwargs)
    

    # def apply_rotation_symmetry(self, vmobject: VMobject, i: int) -> VMobject:
    #     vmobject.shift(-self.star_center)
    #     vmobject.rotate_about_origin(TAU * i / self.n)
    #     vmobject.shift(self.star_center)
    #     return vmobject


