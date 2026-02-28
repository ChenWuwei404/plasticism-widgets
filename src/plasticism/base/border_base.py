from pygame.typing import ColorLike

from plasticism.core.surface_clip import SurfaceClip
from plasticism.gui import Widget
from abc import ABC, abstractmethod

from plasticism.core.draw import rect_outline

class BorderBase(Widget, ABC):
    @abstractmethod
    def get_border_color(self) -> ColorLike:...

    @abstractmethod
    def get_border_width(self) -> int:...

    def draw_border(self, clip: SurfaceClip) -> None:
        rect_outline(clip, self.get_border_color(), (0, 0, self.get_visual_width(), self.get_visual_height()), self.get_border_width())