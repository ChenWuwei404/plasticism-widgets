from typing import Optional, Tuple
from pygame.typing import ColorLike

from pygame import freetype
freetype.init()

from pygame.freetype import Font, SysFont, match_font
from pygame import Surface, Rect, SRCALPHA

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
        width = font.get_rect(text).width
        height = self.get_height(size)
        surface = Surface((width, height), SRCALPHA)
        font.render_to(surface, (0, 0), text, color, background, size=size * scale)
        return surface
    
    def render_to(self, surface: Surface, pos: tuple[int, int], text: str, color: ColorLike, background: Optional[ColorLike] = None, italic: bool = False, bold: bool = False, size = 0, scale = 1.0) -> Rect:
        font = self.get_font(italic=italic, bold=bold)
        return font.render_to(surface, pos, text, color, background, size=size * scale)
    
    def get_height(self, size: float = 0) -> int:
        return self.regular.get_sized_height(size)
    
    def get_ascender(self, size: float = 0) -> int:
        return self.regular.get_sized_ascender(size)
    
    def get_descender(self, size: float = 0) -> int:
        return self.regular.get_sized_descender(size)
    
    def support(self, text: str) -> bool:
        return all(self.regular.get_metrics(char)[0] is not None for char in text)

