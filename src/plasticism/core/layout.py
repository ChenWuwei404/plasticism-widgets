from typing import TYPE_CHECKING, Optional
from enum import Enum

if TYPE_CHECKING:
    from plasticism.gui.widget import Widget

class Position(Enum):
    """
    STATIC: The position of the widget is determined by the layout of its parent widget. It will be arranged in the order it is added to the parent widget.
    ABSOLUTE: The position of the widget is determined by its own layout. It will be arranged according to the coordinates returned by the `get_layout`-series methods.
    """
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

    Child widgets call `get_layout`-series methods to get their layout areas.

    Parent widgets call `get_content`-series methods to get the minimum required content area for their children widgets, and call `update` method to update the layout when necessary.
    """
    def __init__(self, widget: 'Widget') -> None:
        self.widget = widget

    def update(self) -> None:
        pass

    def get_content_width(self) -> int:
        """
        Called by a widget to get minimum required width of the content area.
        """
        return 0
    
    def get_content_height(self) -> int:
        """
        Called by a widget to get minimum required height of the content area.
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