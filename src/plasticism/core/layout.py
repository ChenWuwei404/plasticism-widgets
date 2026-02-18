from typing import TYPE_CHECKING, Optional
from enum import Enum

if TYPE_CHECKING:
    from plasticism.gui.widget import Widget

class Position(Enum):
    STATIC = 0
    ABSOLUTE = 1

class AlignHorizontal(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2

class AlignVertical(Enum):
    TOP = 0
    MIDDLE = 1
    BOTTOM = 2

def minimum(*args: Optional[int]) -> int:
    return min([arg for arg in args if arg is not None], default=0)

def maximum(*args: Optional[int]) -> int:
    return max([arg for arg in args if arg is not None], default=0)

class Layout:
    """
    Layout defines how the content of a widget is arranged and how the layout of its children widgets is determined.
    """
    def __init__(self, widget: 'Widget') -> None:
        self.widget = widget

    def update(self) -> None:
        pass

    def get_content_width(self) -> int:
        """
        Called by a widget to get mininum required width of the content area.
        """
        return 0
    
    def get_content_height(self) -> int:
        """
        Called by a widget to get mininum required height of the content area.
        """
        return 0
    
    def get_layout_x(self, widget: 'Widget') -> int:
        """
        Called by a child widget to get the x coordinate of the top-left corner of its layout area relative to the top-left corner of the content area of its parent widget.
        """
        return 0
    
    def get_layout_y(self, widget: 'Widget') -> int:
        """
        Called by a child widget to get the y coordinate of the top-left corner of its layout area relative to the top-left corner of the content area of its parent widget.
        """
        return 0
    
    def get_layout_width(self, widget: 'Widget') -> int:
        """
        Called by a child widget to get the width of its layout area.
        """
        return self.widget.get_content_width()
    
    def get_layout_height(self, widget: 'Widget') -> int:
        """
        Called by a child widget to get the height of its layout area.
        """
        return self.widget.get_content_height()