from typing import Optional, Tuple, Sequence
from pygame.typing import ColorLike

from pygame import freetype, draw
freetype.init()

from pygame.freetype import Font, SysFont, match_font
from pygame import Surface, Rect, SRCALPHA

from functools import lru_cache

from plasticism.core.word import Element, parse
from plasticism.core.surface_clip import SurfaceLike

class Metrics:
    def __init__(self, metrics: Sequence[Optional[Tuple[int, int, int, int, float, float]]]) -> None:
        self.metrics = metrics

    def get_min_x(self) -> int:
        return self.metrics[0][0] if self.metrics and self.metrics[0] else 0
    
    def get_max_x(self) -> int:
        return self.metrics[-1][1] if self.metrics and self.metrics[-1] else 0
    
    def get_min_y(self) -> int:
        return min(m[2] for m in self.metrics if m)
    
    def get_max_y(self) -> int:
        return max(m[3] for m in self.metrics if m)
    
    def get_advance_x(self) -> float:
        return sum(m[4] for m in self.metrics if m)
    
    def get_advance_y(self) -> float:
        return sum(m[5] for m in self.metrics if m)
    
@lru_cache(256)
def get_metrics(font: Font, text: str, size: int, scale: float) -> Metrics:
    return Metrics(font.get_metrics(text, size * scale))

class FontSeries:
    def __init__(self, regular: Font, bold: Optional[Font] = None, italic: Optional[Font] = None, bold_italic: Optional[Font] = None) -> None:
        self.regular = regular
        self.bold = bold
        self.italic = italic
        self.bold_italic = bold_italic

    @classmethod
    def from_names(cls, size: int, regular_name: str, bold_name: Optional[str] = None, italic_name: Optional[str] = None, bold_italic_name: Optional[str] = None) -> 'FontSeries':
        regular = SysFont(regular_name, size)
        bold = SysFont(bold_name, size) if bold_name else None
        italic = SysFont(italic_name, size) if italic_name else None
        bold_italic = SysFont(bold_italic_name, size) if bold_italic_name else None
        return cls(regular, bold, italic, bold_italic)

    @classmethod
    def from_files(cls, size: int, regular_file: str, bold_file: Optional[str] = None, italic_file: Optional[str] = None, bold_italic_file: Optional[str] = None) -> 'FontSeries':
        regular = Font(regular_file, size)
        bold = Font(bold_file, size) if bold_file else None
        italic = Font(italic_file, size) if italic_file else None
        bold_italic = Font(bold_italic_file, size) if bold_italic_file else None
        return cls(regular, bold, italic, bold_italic)

    @property
    def size(self) -> float | tuple[float, float]:
        return self.regular.size
    
    @size.setter
    def size(self, value: float | tuple[float, float]) -> None:
        self.regular.size = value
        if self.bold:
            self.bold.size = value
        if self.italic:
            self.italic.size = value
        if self.bold_italic:
            self.bold_italic.size = value

    def get_regular(self) -> Font:
        return self.regular
    
    def get_bold(self) -> Font:
        return self.bold if self.bold else self.regular
    
    def get_italic(self) -> Font:
        return self.italic if self.italic else self.regular
    
    def get_bold_italic(self) -> Font:
        return self.bold_italic if self.bold_italic else self.get_bold()
    
    def get_font(self, italic: bool = False, bold: bool = False) -> Font:
        if bold and italic:
            return self.get_bold_italic()
        elif bold:
            return self.get_bold()
        elif italic:
            return self.get_italic()
        else:
            return self.get_regular()
    
    def render(self, text: str, color: ColorLike, background: Optional[ColorLike] = None, italic: bool = False, bold: bool = False, size = 0, scale = 1.0) -> Surface:
        font = self.get_font(italic=italic, bold=bold)
        metric = get_metrics(font, text, size, scale)
        width = metric.get_advance_x()
        height = self.get_height(size, scale)
        surface = Surface((width, height), SRCALPHA)
        font.render_to(surface, (metric.get_min_x(), self.get_ascender(size, scale) - metric.get_max_y()), text, color, background, size=size * scale)
        return surface
    
    def render_to(self, surface: SurfaceLike, pos: tuple[int, int], text: str, color: ColorLike, background: Optional[ColorLike] = None, italic: bool = False, bold: bool = False, size = 0, scale = 1.0) -> Rect:
        font = self.get_font(italic=italic, bold=bold)
        metric = get_metrics(font, text, size, scale)
        if background:
            width = metric.get_advance_x()
            height = self.get_height(size, scale)
            surface.fill(background, (pos, (width, height)))
        if isinstance(surface, Surface):
            font.render_to(surface, (pos[0] + metric.get_min_x(), pos[1] + self.get_ascender(size, scale) - metric.get_max_y()), text, color, size=size * scale)
        else:
            offset_x, offset_y = surface.get_blit_offset()
            font.render_to(surface.surface, (pos[0] + metric.get_min_x() + offset_x, pos[1] + self.get_ascender(size, scale) - metric.get_max_y() + offset_y), text, color, size=size * scale)
        return Rect(pos, (metric.get_advance_x(), self.get_height(size, scale)))
    
    def get_rect(self, text: str, italic: bool = False, bold: bool = False, size = 0, scale = 1.0) -> Rect:
        font = self.get_font(italic=italic, bold=bold)
        metric = get_metrics(font, text, size, scale)
        width = metric.get_advance_x()
        height = self.get_height(size, scale)
        return Rect((0, 0), (width, height))

    def get_height(self, size: float = 0, scale: float = 1.0) -> int:
        return self.regular.get_sized_height(size * scale)
    
    def get_ascender(self, size: float = 0, scale: float = 1.0) -> int:
        return self.regular.get_sized_ascender(size * scale)
    
    def get_descender(self, size: float = 0, scale: float = 1.0) -> int:
        return self.regular.get_sized_descender(size * scale)
    
    def support(self, text: str) -> bool:
        return all(self.regular.get_metrics(char)[0] is not None for char in text)


class FontFamily:
    def __init__(self, *args: FontSeries) -> None:
        self.font_series = list(args)

    @classmethod
    def from_names(cls, size: int, *names: Tuple[str, Optional[str], Optional[str], Optional[str]]) -> 'FontFamily':
        return cls(*[FontSeries.from_names(size, *name) for name in names if match_font(name[0])])
    
    @classmethod
    def from_files(cls, size: int, *files: Tuple[str, Optional[str], Optional[str], Optional[str]]) -> 'FontFamily':
        return cls(*[FontSeries.from_files(size, *file) for file in files if file[0]])
    
    @property
    def size(self) -> float | tuple[float, float]:
        return self.font_series[0].size
    
    @size.setter
    def size(self, value: float | tuple[float, float]) -> None:
        for font_series in self.font_series:
            font_series.size = value

    def find_font(self, element: Element) -> FontSeries:
        for font_series in self.font_series:
            if font_series.support(element):
                return font_series
        return self.font_series[-1]

    def render(self, text: str, color: ColorLike, background: Optional[ColorLike] = None, italic: bool = False, bold: bool = False, size = 0, scale = 1.0) -> Surface:
        elements = parse(text)
        width = sum(self.find_font(element).get_rect(element, italic=italic, bold=bold, size=size, scale=scale).width for element in elements)
        height = self.get_height(size, scale)
        surface = Surface((width, height), SRCALPHA)
        self.render_to(surface, (0, 0), text, color, background, italic=italic, bold=bold, size=size, scale=scale)
        return surface
    
    def render_to(self, surface: SurfaceLike, pos: tuple[int, int], text: str, color: ColorLike, background: Optional[ColorLike] = None, italic: bool = False, bold: bool = False, size = 0, scale = 1.0) -> Rect:
        elements = parse(text)
        x = pos[0]
        if background:
            width = sum(self.find_font(element).get_rect(element, italic=italic, bold=bold, size=size, scale=scale).width for element in elements)
            height = self.get_height(size, scale)
            surface.fill(background, (pos, (width, height)))
        for element in elements:
            font_series = self.find_font(element)
            x += font_series.render_to(surface, (x, pos[1]), element, color, size=size, scale=scale).width
        return Rect(pos, (x - pos[0], self.get_height(size, scale)))
    
    def get_rect(self, text: str, italic: bool = False, bold: bool = False, size = 0, scale = 1.0) -> Rect:
        elements = parse(text)
        width = sum(self.find_font(element).get_rect(element, italic=italic, bold=bold, size=size, scale=scale).width for element in elements)
        height = self.get_height(size, scale)
        return Rect((0, 0), (width, height))

    def get_height(self, size: float = 0, scale: float = 1.0) -> int:
        return max(font_series.get_height(size, scale) for font_series in self.font_series)
    
    def get_ascender(self, size: float = 0, scale: float = 1.0) -> int:
        return max(font_series.get_ascender(size, scale) for font_series in self.font_series)
    
    def get_descender(self, size: float = 0, scale: float = 1.0) -> int:
        return min(font_series.get_descender(size, scale) for font_series in self.font_series)

FontLike = FontSeries | FontFamily

import sys
if sys.platform == 'win32':
    default_font = FontFamily(
        FontSeries.from_files(16,
                              r'C:\Windows\Fonts\arial.ttf',
                              r'C:\Windows\Fonts\arialbd.ttf',
                              r'C:\Windows\Fonts\ariali.ttf',
                              r'C:\Windows\Fonts\arialbi.ttf'),
        FontSeries.from_files(16,
                              r'C:\Windows\Fonts\simhei.ttf',
                              ),
        )
elif sys.platform == 'darwin':
    default_font = FontSeries.from_names(16, 'PingFang SC')
else:
    default_font = FontSeries.from_names(16, 'DejaVu Sans')