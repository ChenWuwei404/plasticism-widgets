from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plasticism.gui.widget import Widget

class Layout:
    def __init__(self, widget: 'Widget') -> None:
        self.widget = widget

    def update(self) -> None:
        pass

    def get_content_width(self) -> int:
        return self.widget.get_content_width()
    
    def get_content_height(self) -> int:
        return self.widget.get_content_height()
    
    def get_layout_x(self, widget: 'Widget') -> int:
        return widget.x
    
    def get_layout_y(self, widget: 'Widget') -> int:
        return widget.y
    
    def get_layout_width(self, widget: 'Widget') -> int:
        return self.widget.get_content_width()
    
    def get_layout_height(self, widget: 'Widget') -> int:
        return self.widget.get_content_height()