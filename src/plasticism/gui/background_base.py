from pygame.typing import ColorLike

from plasticism.core.surface_clip import SurfaceClip
from plasticism.gui import Widget
from abc import ABC, abstractmethod

class BackgroundBase(Widget, ABC):
    @abstractmethod
    def get_background_color(self) -> ColorLike:...

    def draw_background(self, clip: SurfaceClip) -> None:
        clip.fill(self.get_background_color())