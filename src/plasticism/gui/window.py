from typing import Optional

import pygame

from pygame import display
from pygame import Surface, SRCALPHA
from pygame import Color

from plasticism.gui.widget import Widget
from plasticism.core.event import Event, generate_event

import sys
if sys.platform == "win32":
    from plasticism.core.system import set_titlebar_color, set_border_color

class Window:
    def __init__(self, size: tuple[int, int], flags: int = 0, vsync: int = 0) -> None:
        pygame.init() if not pygame.get_init() else None

        self.size = size
        display.set_mode(size, flags=flags, vsync=vsync)
        self.hwnd = display.get_wm_info()["window"]
        self.set_title("Plasticism Window")
        self.set_icon(Surface((0, 0), SRCALPHA))
        self.set_running(True)
        if sys.platform == "win32":
            self.set_titlebar_color(None)
            self.set_border_color(Color(64, 64, 64))

    def set_title(self, title: str) -> None:
        self.title = title
        display.set_caption(title)

    def set_icon(self, icon: Surface) -> None:
        self.icon = icon
        display.set_icon(icon)

    def set_titlebar_color(self, color: Optional[Color]) -> None:
        """
        Only available on Windows.
        """
        self.titlebar_color = color
        set_titlebar_color(self.hwnd, color)

    def set_border_color(self, color: Optional[Color]) -> None:
        """
        Only available on Windows.
        """
        self.border_color = color
        set_border_color(self.hwnd, color)


    def set_running(self, running: bool) -> None:
        self.running = running
    
    def set_root_widget(self, widget: Widget) -> None:
        self.root_widget = widget

    def exec(self) -> None:
        while self.running:
            for py_event in pygame.event.get():
                event = generate_event(py_event)
                self.root_widget.tunnel_event(event)

    
    def exit(self) -> None:
        display.quit()
