from typing import Optional

from plasticism.core.event import Event, EventBundle, Processor, UniversalEvent, KeyEvent, TextEvent, LocalEvent, SpreadEvent, GlobalEvent, MouseEvent
from plasticism.core.assigner import Assigner, AssignerItem
from plasticism.core.trigger import Trigger

class MouseEnter(LocalEvent, MouseEvent):
    pass

class MouseLeave(LocalEvent, MouseEvent):
    pass

class Widget:
    def __init__(self) -> None:
        self.parent: Optional[Widget] = None
        self.children: list[Widget] = []

        self.event_processors: list[Processor] = []

        self.assigner = Assigner()
        self.mouse_enter = AssignerItem(MouseEnter)
        self.assigner.add_item(self.mouse_enter)
        self.mouse_leave = AssignerItem(MouseLeave)
        self.assigner.add_item(self.mouse_leave)

        self.on_mouse_enter = Trigger(MouseEnter)
        self.mouse_enter.connect(self.on_mouse_enter)
        self.on_mouse_leave = Trigger(MouseLeave)
        self.mouse_leave.connect(self.on_mouse_leave)

    def is_mouse_focused(self) -> bool:
        return False
    
    def is_keyboard_focused(self) -> bool:
        return False

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
    
    def event_filter(self, event: Event) -> bool:
        return False
    
    def event_fetch_checker(self, event: Event) -> bool:
        return False
    
    def create_event_bundle(self, event: Event) -> EventBundle:
        return EventBundle([event])

    def process_events(self, event_bundle: EventBundle) -> None:
        [processor.process_event(event_bundle) for processor in self.event_processors]

    def assign_events(self, event_bundle: EventBundle) -> None:
        self.assigner.process_event(event_bundle)

    def bubble_event(self, event: Event) -> None:
        if self.parent:
            if isinstance(event, LocalEvent):
                return
            if isinstance(event, SpreadEvent) and event.wrap is self:
                return
            if isinstance(event, GlobalEvent) and event.handled:
                return
            self.get_parent().handle_event(event)
    
    def handle_event(self, event: Event) -> None:
        bundle = self.create_event_bundle(event)
        self.process_events(bundle)
        self.assign_events(bundle)
        [self.bubble_event(e) for e in bundle]
    
    def tunnel_event(self, event: Event) -> None:
        if self.event_filter(event):
            return
        if self.event_fetch_checker(event):
            self.handle_event(event)
        
        if isinstance(event, UniversalEvent):
            [child.tunnel_event(event) for child in self.get_children()]
        elif isinstance(event, MouseEvent):
            focused_child = next((child for child in self.get_children() if child.is_mouse_focused()), None)
            if focused_child:
                focused_child.tunnel_event(event)
        elif isinstance(event, KeyEvent) or isinstance(event, TextEvent):
            focused_child = next((child for child in self.get_children() if child.is_keyboard_focused()), None)
            if focused_child:
                focused_child.tunnel_event(event)