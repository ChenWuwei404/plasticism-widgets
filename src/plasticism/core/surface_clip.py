from typing import Union, Optional

from pygame import Surface, Rect, Vector2, Color

SurfaceLike = Union[Surface, 'SurfaceClip']
Point = tuple[float, float]

def offset_rect(rect: Rect, offset: Vector2) -> Rect:
    return Rect(rect.x + offset.x, rect.y + offset.y, rect.width, rect.height)

class SurfaceClip:
    def __init__(self, surface: Surface, clip_rect: Optional[Rect] = None, parent: Optional['SurfaceClip'] = None) -> None:
        self.surface = surface
        self.clip_rect = clip_rect if clip_rect else surface.get_rect()
        self.parent_clip: Optional['SurfaceClip'] = parent

    def blit(self, source: SurfaceLike, dest: Point = (0, 0)) -> None:
        dest_vector = Vector2(*dest)
        blit_offset = Vector2(*self.clip_rect.topleft)
        surface_pos = dest_vector + blit_offset
        if isinstance(source, SurfaceClip):
            surface_pos += Vector2(*source.clip_rect.topleft)
            self.surface.blit(source.surface, surface_pos, source.clip_rect)
        else:
            self.surface.blit(source, surface_pos)

    def fill(self, color: Color, rect: Union[Rect, None] = None) -> None:
        if rect is None:
            self.surface.fill(color, self.clip_rect)
        else:
            dest_vector = Vector2(*rect.topleft)
            blit_offset = Vector2(*self.clip_rect.topleft)
            blit_pos = dest_vector + blit_offset
            self.surface.fill(color, Rect(blit_pos.x, blit_pos.y, rect.width, rect.height))

    def subclip(self, rect: Rect) -> 'SurfaceClip':
        rect = offset_rect(rect, Vector2(*self.clip_rect.topleft))
        surface_rect = rect.clip(self.surface.get_rect())
        if surface_rect.width == 0 or surface_rect.height == 0:
            return SurfaceClip(Surface((0, 0)), Rect(0, 0, 0, 0))
        else:
            return SurfaceClip(self.surface.subsurface(surface_rect), parent=self)
        
    def get_parent(self) -> Optional['SurfaceClip']:
        return self.parent_clip

    def get_width(self) -> int:
        return self.clip_rect.width
    
    def get_height(self) -> int:
        return self.clip_rect.height
    
    def get_size(self) -> tuple[int, int]:
        return (self.get_width(), self.get_height())
    
    @property
    def width(self) -> int:
        return self.get_width()
    
    @property
    def height(self) -> int:
        return self.get_height()
    
    @property
    def size(self) -> tuple[int, int]:
        return self.get_size()
