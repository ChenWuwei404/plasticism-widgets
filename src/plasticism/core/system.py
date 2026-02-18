import sys
import ctypes

from pygame import Color
from typing import Optional

if sys.platform == "win32":
    from ctypes import wintypes
    dwmapi = ctypes.windll.dwmapi
    user32 = ctypes.windll.user32

    def get_window_dpi_scale(hwnd: int) -> float:
        awareness = ctypes.c_int(2)  # PROCESS_PER_MONITOR_DPI_AWARE
        ctypes.windll.shcore.SetProcessDpiAwareness(awareness)

        dpi = user32.GetDpiForWindow(hwnd)
        return dpi / 96.0  # 96 DPI is the default scale (100%)

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
    import subprocess
    def get_window_dpi_scale(hwnd: int) -> float:
        try:
            result = subprocess.run(
                ['xrdb', '-query'],
                capture_output=True, text=True
            )
            for line in result.stdout.split('\n'):
                if 'Xft.dpi' in line:
                    dpi = int(line.split(':')[-1].strip())
                    return dpi / 96.0
        except Exception:
            pass
        return 1.0

elif sys.platform == "macos":
    pass
    # TODO: Implement for macOS platforms