from typing import Optional

from plasticism.core.event import Event, EventBundle, Processor, UniversalEvent, KeyEvent, TextEvent, LocalEvent, SpreadEvent, GlobalEvent, MouseEvent
from plasticism.core.assigner import Assigner, AssignerItem
from plasticism.core.trigger import Trigger

class MouseEnter(LocalEvent, MouseEvent):
    pass

class MouseLeave(LocalEvent, MouseEvent):
    pass

class Widget:
    """
    Base class for all GUI widgets.

    ## Event System

    ### Usage

    Call `Widget.tunnel_event(event)` to start event handling
    
    The event system in Plasticism GUI is designed to handle various types of events efficiently and flexibly. Widgets can process events through a series of steps including filtering, fetching, processing, assigning, and bubbling.

    ### Steps
    
    1. **Event Filtering**: Each widget can implement the `event_filter_checker` method to determine whether to filter out specific events. If an event is filtered out, it will not be processed further by that widget.
    2. **Event Fetching**: The `event_fetch_checker` method allows widgets to decide whether to fetch an event for processing. If an event is fetched, it will be handled by the widget itself rather than being passed directly to its children.
    3. **Event Processing**: Widgets can have multiple event processors that handle events in `Widget.event_processors`. The `process_events` method iterates through all registered processors to process the event bundle.
    4. **Event Assigning**: The `assign_events` method uses an `Assigner` to manage event assignments. This allows for dynamic event handling based on the widget's configuration.
    5. **Event Bubbling**: After processing, events can be bubbled up to parent widgets using the `bubble_event` method. This allows parent widgets to respond to events that were not fully handled by their children. Even can it used to spread signals to parent widgets.
    
    """
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
    
    def event_filter_checker(self, event: Event) -> bool:
        """
        Check whether to filter out the event.
        
        :param event: an Event to be checked
        :type event: Event
        :return: `True` if the event is to be filtered out
        :rtype: bool
        """
        return False
    
    def event_fetch_checker(self, event: Event) -> bool:
        """
        Check whether to fetch the event.

        *fetch* means to handle the event at this widget and not pass it directly to children.
        
        :param event: an Event to be checked
        :type event: Event
        :return: `True` if the event is to be fetched
        :rtype: bool
        """
        return False
    
    def create_event_bundle(self, event: Event) -> EventBundle:
        return EventBundle([event])

    def process_events(self, event_bundle: EventBundle) -> None:
        [processor.process_event(event_bundle) for processor in self.event_processors]

    def assign_events(self, event_bundle: EventBundle) -> None:
        self.assigner.process_event(event_bundle)

    def bubble_event(self, event: Event) -> None:
        """
        Bubble an event up to the parent widget if needed.
        
        :param event: an Event to be checked and bubbled
        :type event: Event
        """
        if self.parent:
            if isinstance(event, LocalEvent):
                return
            if isinstance(event, SpreadEvent) and event.wrap is self:
                return
            if isinstance(event, GlobalEvent) and event.handled:
                return
            self.get_parent().handle_event(event)
    
    def handle_event(self, event: Event) -> None:
        """
        Process an Event in this widget.
        
        :param event: an Event to be handled
        :type event: Event
        """
        bundle = self.create_event_bundle(event)
        self.process_events(bundle)
        self.assign_events(bundle)
        [self.bubble_event(e) for e in bundle]
    
    def tunnel_event(self, event: Event) -> None:
        """
        Tunnel an event through this widget to its children.

        IMPORTANT: Parent widgets should call this method of thier children to propagate events.
        
        :param event: an Event to be tunnelled
        :type event: Event
        """
        if self.event_filter_checker(event):
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