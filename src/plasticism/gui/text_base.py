from typing import Optional
from pygame.typing import ColorLike
from plasticism.core.font import FontLike, default_font

from plasticism.gui import Widget
from abc import ABC, abstractmethod

class TextBase(Widget, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.font_size = 16
        self.font: Optional[FontLike] = None
    
    @abstractmethod
    def get_text(self) -> str:...

    @abstractmethod
    def set_text(self, text: str) -> None:...

    @abstractmethod
    def get_text_x(self) -> int:...

    @abstractmethod
    def get_text_y(self) -> int:...

    @abstractmethod
    def get_color(self) -> ColorLike:...

    def set_font_size(self, font_size: int) -> None:
        self.font_size = font_size

    def get_font_size(self) -> int:
        return self.font_size
    
    def set_font(self, font: Optional[FontLike]) -> None:
        self.font = font
    
    def get_font(self) -> FontLike:
        return self.font or default_font