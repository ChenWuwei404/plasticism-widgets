import sys
import ctypes

from pygame import Color
from typing import Optional

if sys.platform == "win32":
    from ctypes import wintypes
    dwmapi = ctypes.windll.dwmapi

    def _color_to_ref(color: Color) -> int:
        return (color.b << 16) | (color.g << 8) | color.r

    def set_titlebar_color(hwnd: int, color: Optional[Color]):
        if color:
            color_ref = _color_to_ref(color)
        else:
            color_ref = 0xFFFFFFFE  # Default color
        try:
            DWMWA_CAPTION_COLOR = 35
            # DWMWA_TEXT_COLOR = 36
            
            dwmapi.DwmSetWindowAttribute(
                wintypes.HWND(hwnd),
                DWMWA_CAPTION_COLOR,
                ctypes.byref(wintypes.DWORD(color_ref)),
                ctypes.sizeof(wintypes.DWORD)
            )
        except Exception as e:
            print(e)

    def set_border_color(hwnd: int, color: Optional[Color]):
        if color:
            color_ref = _color_to_ref(color)
        else:
            color_ref = 0xFFFFFFFE  # Transparent color
        try:
            DWMWA_BORDER_COLOR = 34
            print(dwmapi.DwmSetWindowAttribute(
                wintypes.HWND(hwnd),
                DWMWA_BORDER_COLOR,
                ctypes.byref(wintypes.DWORD(color_ref)),
                ctypes.sizeof(wintypes.DWORD)
            ))
        except Exception as e:
            print(e)

elif sys.platform == "linux":
    pass
    # TODO: Implement for Linux platforms

elif sys.platform == "macos":
    pass
    # TODO: Implement for macOS platforms