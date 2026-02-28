from plasticism.core.surface_clip import SurfaceClip
from pygame.typing import ColorLike, RectLike
from pygame import Rect
from pygame import draw as pygame_draw

def rect_filled(surface_clip: SurfaceClip, color: ColorLike, rect: RectLike):
    rect = Rect(rect)
    surface = surface_clip.surface
    pygame_rect = Rect(
        rect.x + surface_clip.clip_rect.x,
        rect.y + surface_clip.clip_rect.y,
        rect.width,
        rect.height,
    )
    surface.fill(color, pygame_rect)

def rect_outline(surface_clip: SurfaceClip, color: ColorLike, rect: RectLike, width: int):
    rect = Rect(rect)
    surface = surface_clip.surface
    pygame_rect = Rect(
        rect.x + surface_clip.clip_rect.x,
        rect.y + surface_clip.clip_rect.y,
        rect.width,
        rect.height,
    )
    pygame_draw.rect(surface, color, pygame_rect, width)