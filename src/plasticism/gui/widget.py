from typing import Optional

from plasticism.core.event import LocalEvent, MouseEvent

class MouseEnter(LocalEvent, MouseEvent):
    pass

class MouseLeave(LocalEvent, MouseEvent):
    pass

class Widget:
    def __init__(self) -> None:
        self.parent: Optional[Widget] = None
        self.children: list[Widget] = []

    def set_parent(self, parent: Optional['Widget']) -> None:
        self.parent = parent

    def get_parent(self) -> 'Widget':
        if self.parent is None:
            raise ValueError(f"{repr(self)} has no parent.")
        return self.parent
    
    def add_child(self, child: 'Widget') -> None:
        child.set_parent(self)
        self.children.append(child)

    def remove_child(self, child: 'Widget') -> None:
        child.set_parent(None)
        self.children.remove(child)

    def get_children(self) -> list['Widget']:
        return self.children