from typing import Optional

import pygame

from pygame import display
from pygame import Surface, SRCALPHA
from pygame import Color
from pygame import Rect

from plasticism.gui.widget import Widget
from plasticism.core.event import Event, generate_event
from plasticism.core.surface_clip import SurfaceClip

import sys
if sys.platform == "win32":
    from plasticism.core.system import set_titlebar_color, set_border_color, get_window_dpi_scale
elif sys.platform == "linux":
    from plasticism.core.system import get_window_dpi_scale

class Window:
    def __init__(self, size: tuple[int, int], widget: Widget, flags: int = 0, vsync: int = 0) -> None:
        pygame.init() if not pygame.get_init() else None
        self.set_root_widget(widget)

        self.set_size(size)
        self.screen = display.set_mode(self.size, flags=flags, vsync=vsync)
        self.hwnd = display.get_wm_info()["window"]
        self.set_title("Plasticism Window")
        self.set_icon(Surface((0, 0), SRCALPHA))
        self.set_running(True)
        if sys.platform == "win32":
            self.set_titlebar_color(None)
            # self.set_border_color(Color(64, 64, 64))
        self.clock = pygame.time.Clock()

    def get_dpi_scale(self) -> float:
        if sys.platform == "win32":
            return get_window_dpi_scale(self.hwnd)
        return 1.0

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
        if sys.platform != "win32":
            return
        self.titlebar_color = color
        set_titlebar_color(self.hwnd, color)

    def set_border_color(self, color: Optional[Color]) -> None:
        """
        Only available on Windows.
        """
        if sys.platform != "win32":
            return
        self.border_color = color
        set_border_color(self.hwnd, color)

    def set_size(self, size: tuple[int, int], resized: bool = True) -> None:
        self.size = size
        self.root_widget.set_max_size(size)
        display.set_mode(size) if not resized else None

    def set_running(self, running: bool) -> None:
        self.running = running
    
    def set_root_widget(self, widget: Widget) -> None:
        self.root_widget = widget
        self.root_widget.set_size((-1, -1))

    def exec(self) -> None:
        while self.running:
            self.process()
            self.update(self.clock.tick() / 1000)
            self.render()

    def update_scale_factor(self):
        self.root_widget.set_scale_factor(self.get_dpi_scale())

    def close(self) -> None:
        self.set_running(False)

    def get_main_clip(self) -> SurfaceClip:
        return SurfaceClip(self.screen, Rect(0, 0, *self.size))

    def render(self) -> None:
        self.root_widget.draw(self.get_main_clip())
        display.flip()

    def process(self) -> None:
        self.update_scale_factor()
        for pg_event in pygame.event.get():
            if pg_event.type == pygame.VIDEORESIZE:
                self.set_size((pg_event.w, pg_event.h), resized=True)
            event = generate_event(pg_event)
            self.root_widget.tunnel_event(event)

    def update(self, dt: float) -> None:
        self.root_widget.update(dt)
    
    def exit(self) -> None:
        display.quit()
