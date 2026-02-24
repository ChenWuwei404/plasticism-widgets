from typing import Optional
from pygame.typing import ColorLike

from plasticism.core.surface_clip import SurfaceClip
from plasticism.core.layout import AlignHorizontal, AlignVertical
from plasticism.core.font import FontLike, default_font

from plasticism.gui import Widget


class Label(Widget):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        self.text_align_horizontal = AlignHorizontal.LEFT
        self.text_align_vertical = AlignVertical.TOP
        self.font_size = 16
        self.font: Optional[FontLike] = None

    def get_min_height(self) -> int:
        return max(super().get_min_height(), self.get_text_height() + self.padding_top + self.padding_bottom)
    
    def get_min_width(self) -> int:
        return max(super().get_min_width(), self.get_text_width() + self.padding_left + self.padding_right)

    def set_text(self, text: str) -> None:
        self.text = text

    def get_text(self) -> str:
        return self.text
    
    def set_font_size(self, font_size: int) -> None:
        self.font_size = font_size

    def get_font_size(self) -> int:
        return self.font_size
    
    def set_font(self, font: Optional[FontLike]) -> None:
        self.font = font
    
    def get_font(self) -> FontLike:
        return self.font or default_font
    
    def get_text_width(self) -> int:
        return self.get_font().get_rect(self.text, size=self.font_size, scale=self.get_scale_factor()).width
    
    def get_text_height(self) -> int:
        return self.get_font().get_rect(self.text, size=self.font_size, scale=self.get_scale_factor()).height
    
    def get_text_x(self) -> int:
        return 0 if self.text_align_horizontal == AlignHorizontal.LEFT else \
            (self.get_width() - self.get_text_width()) // 2 if self.text_align_horizontal == AlignHorizontal.CENTER else \
            self.get_width() - self.get_text_width()
    
    def get_text_y(self) -> int:
        return 0 if self.text_align_vertical == AlignVertical.TOP else \
            (self.get_height() - self.get_text_height()) // 2 if self.text_align_vertical == AlignVertical.MIDDLE else \
            self.get_height() - self.get_text_height()
    
    def get_color(self) -> ColorLike:
        return (255, 255, 255)

    def draw_content(self, clip: SurfaceClip) -> None:
        self.get_font().render_to(clip.surface, (self.get_text_x(), self.get_text_y()), self.text, self.get_color(), size=self.font_size, scale=self.get_scale_factor())

class FixedScaleLabel(Label):
    def draw_content(self, clip: SurfaceClip) -> None:
        self.get_font().render_to(clip.surface, (self.get_text_x(), self.get_text_y()), self.text, self.get_color(), size=self.font_size)