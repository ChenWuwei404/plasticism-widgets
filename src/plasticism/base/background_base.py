from pygame.typing import ColorLike

from plasticism.core.surface_clip import SurfaceClip
from plasticism.base import Widget
from abc import abstractmethod

class BackgroundBase(Widget):
    @abstractmethod
    def get_background_color(self) -> ColorLike:...

    def draw_background(self, clip: SurfaceClip) -> None:
        clip.fill(self.get_background_color())