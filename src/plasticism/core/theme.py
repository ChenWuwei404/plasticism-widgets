from typing import Any, Generic, TypeVar

from dataclasses import dataclass

from plasticism.core.color import Color, Oklch

T = TypeVar('T')

class Item[T]:
    def __init__(self, *args: T) -> None:
        self.args = args

    def __getitem__(self, index: int) -> T:
        return self.args[index]

class ColorItem(Item[Color]):
    pass

class SizeItem(Item[int]):
    pass
    

@dataclass
class Theme:
    background: ColorItem
    foreground: ColorItem

    background_error: ColorItem
    foreground_error: ColorItem
    background_warning: ColorItem
    foreground_warning: ColorItem
    background_success: ColorItem
    foreground_success: ColorItem

    background_accent: ColorItem
    foreground_accent: ColorItem

    content_size: SizeItem
    title_size: SizeItem

    radius: SizeItem
    space: SizeItem

default_theme = Theme(
    ColorItem(
        Oklch(0.1, 0.01, 215),
        Oklch(0.2, 0.01, 215),
        Oklch(0.3, 0.01, 215),
    ),
    ColorItem(
        Oklch(0.95, 0.01, 215),
        Oklch(0.85, 0.01, 215),
        Oklch(0.7, 0.01, 215),
    ),

    ColorItem(
        Oklch(0.25, 0.05, 15),
        Oklch(0.3, 0.05, 15),
        Oklch(0.35, 0.05, 15),
    ),
    ColorItem(
        Oklch(0.75, 0.15, 15),
        Oklch(0.7, 0.15, 15),
        Oklch(0.65, 0.15, 15),
    ),

    ColorItem(
        Oklch(0.25, 0.05, 60),
        Oklch(0.3, 0.05, 60),
        Oklch(0.35, 0.05, 60),
    ),
    ColorItem(
        Oklch(0.75, 0.15, 60),
        Oklch(0.7, 0.15, 60),
        Oklch(0.65, 0.15, 60),
    ),

    ColorItem(
        Oklch(0.25, 0.05, 150),
        Oklch(0.3, 0.05, 150),
        Oklch(0.35, 0.05, 150),
    ),
    ColorItem(
        Oklch(0.75, 0.15, 150),
        Oklch(0.7, 0.15, 150),
        Oklch(0.65, 0.15, 150),
    ),

    ColorItem(
        Oklch(0.25, 0.05, 240),
        Oklch(0.3, 0.05, 240),
        Oklch(0.35, 0.05, 240),
    ),
    ColorItem(
        Oklch(0.75, 0.15, 240),
        Oklch(0.7, 0.15, 240),
        Oklch(0.65, 0.15, 240),
    ),
    SizeItem(14, 12, 10),
    SizeItem(24, 20, 16),
    SizeItem(12, 8, 4),
    SizeItem(12, 8, 4)
)