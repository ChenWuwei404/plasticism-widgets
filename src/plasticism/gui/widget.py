from typing import Optional

from plasticism.core.event import Event, EventBundle, Processor, UniversalEvent, KeyEvent, TextEvent, LocalEvent, SpreadEvent, GlobalEvent, MouseEvent
from plasticism.core.assigner import Assigner, AssignerItem
from plasticism.core.trigger import Trigger
from plasticism.core.layout import Layout, Position, AlignHorizontal, AlignVertical, minimum, maximum

from pygame import Surface, Rect
from plasticism.core.surface_clip import SurfaceClip

class MouseEnter(LocalEvent, MouseEvent):
    pass

class MouseLeave(LocalEvent, MouseEvent):
    pass

class Widget:
    """
    Base class for all GUI widgets.

    Subclasses should inherit from this class and implement their own rendering and event handling logic.

    ## Layout Properties

    Widgets have various layout properties that control their size and spacing. These properties include width, height, maximum and minimum sizes, padding, and margins.

    Size means the size of the *box*, wrapping padding and content, while margin is outside the box. Occupied size means the size including margin. Just like CSS box model.

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

        # Layout properties

        self.scale_factor = 1.0

        self.layout = Layout(self)

        self.x = 0
        self.y = 0
        self.position: Position = Position.STATIC

        self.align_horizontal: AlignHorizontal = AlignHorizontal.LEFT
        self.align_vertical: AlignVertical = AlignVertical.TOP

        self.width: int = 0  # 0 means shrink to min, negative means stretch to max, positive means fixed size
        self.height: int = 0

        self.max_width: Optional[int] = None
        self.max_height: Optional[int] = None

        self.min_width: int = 0
        self.min_height: int = 0

        self.padding_left: int = 0
        self.padding_right: int = 0
        self.padding_top: int = 0
        self.padding_bottom: int = 0

        self.margin_left: int = 0
        self.margin_right: int = 0
        self.margin_top: int = 0
        self.margin_bottom: int = 0

        # Event system properties

        self.keyboard_focused = False

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

        # Rendering properties

        self.visible = True

    def update(self) -> None:
        self.layout.update()
        for child in self.children:
            child.update()
        

    def set_scale_factor(self, scale_factor: float) -> None:
        self.scale_factor = scale_factor

    def get_scale_factor(self) -> float:
        if self.parent is None:
            return self.scale_factor
        else:
            return self.get_parent().get_scale_factor()

    def get_layout_x(self) -> int:
        return self.get_parent().layout.get_layout_x(self) if self.parent else 0
    
    def get_layout_y(self) -> int:
        return self.get_parent().layout.get_layout_y(self) if self.parent else 0

    def get_layout_width(self) -> int:
        return self.get_parent().layout.get_layout_width(self) if self.parent else self.get_width()
    
    def get_layout_height(self) -> int:
        return self.get_parent().layout.get_layout_height(self) if self.parent else self.get_height()

    def get_x(self) -> int:
        if self.parent is None:
            return self.x
        else:
            return self.get_layout_x() + self.x + (
                0 if self.align_horizontal == AlignHorizontal.LEFT else
                (self.get_layout_width() - self.get_occupied_width()) // 2 if self.align_horizontal == AlignHorizontal.CENTER else
                self.get_layout_width() - self.get_occupied_width()
                )
    
    def get_y(self) -> int:
        if self.parent is None:
            return self.y
        else:
            return self.get_layout_y() + self.y + (
                0 if self.align_vertical == AlignVertical.TOP else
                (self.get_layout_height() - self.get_occupied_height()) // 2 if self.align_vertical == AlignVertical.MIDDLE else
                self.get_layout_height() - self.get_occupied_height()
                )

    def set_max_width(self, max_width: Optional[int]) -> None:
        self.max_width = max_width

    def get_max_width(self) -> int:
        return minimum(self.max_width, (self.get_layout_width() - self.margin_left - self.margin_right) if self.parent else None)

    def set_min_width(self, min_width: int) -> None:
        self.min_width = min_width

    def get_min_width(self) -> int:
        return maximum(self.min_width, self.layout.get_content_width() + self.padding_left + self.padding_right)
    
    def set_max_height(self, max_height: Optional[int]) -> None:
        self.max_height = max_height
    
    def get_max_height(self) -> int:
        return minimum(self.max_height, (self.get_layout_height() - self.margin_top - self.margin_bottom) if self.parent else None)
    
    def set_min_height(self, min_height: int) -> None:
        self.min_height = min_height
    
    def get_min_height(self) -> int:
        return maximum(self.min_height, self.layout.get_content_height() + self.padding_top + self.padding_bottom)
    
    def set_max_size(self, max_size: tuple[Optional[int], Optional[int]]) -> None:
        self.set_max_width(max_size[0])
        self.set_max_height(max_size[1])

    def set_min_size(self, min_size: tuple[int, int]) -> None:
        self.set_min_width(min_size[0])
        self.set_min_height(min_size[1])

    def set_width(self, width: int) -> None:
        self.width = width

    def set_height(self, height: int) -> None:
        self.height = height

    def set_size(self, size: tuple[int, int]) -> None:
        self.set_width(size[0])
        self.set_height(size[1])
    
    def get_width(self) -> int:
        if self.width > 0:
            return self.width
        elif self.width == 0:
            return self.get_min_width()
        else:
            return self.get_max_width()
        
    def get_height(self) -> int:
        if self.height > 0:
            return self.height
        elif self.height == 0:
            return self.get_min_height()
        else:
            return self.get_max_height()
        
    def get_size(self) -> tuple[int, int]:
        return (self.get_width(), self.get_height())

    def set_padding(self, padding: tuple[int, int, int, int]) -> None:
        self.padding_left = padding[0]
        self.padding_top = padding[1]
        self.padding_right = padding[2]
        self.padding_bottom = padding[3]

    def set_margin(self, margin: tuple[int, int, int, int]) -> None:
        self.margin_left = margin[0]
        self.margin_top = margin[1]
        self.margin_right = margin[2]
        self.margin_bottom = margin[3]

    def get_occupied_width(self) -> int:
        return self.get_width() + self.margin_left + self.margin_right
    
    def get_occupied_height(self) -> int:
        return self.get_height() + self.margin_top + self.margin_bottom
    
    def get_occupied_size(self) -> tuple[int, int]:
        return (self.get_occupied_width(), self.get_occupied_height())
    
    def get_content_width(self) -> int:
        return self.get_width() - self.padding_left - self.padding_right
    
    def get_content_height(self) -> int:
        return self.get_height() - self.padding_top - self.padding_bottom
    
    def get_content_size(self) -> tuple[int, int]:
        return (self.get_content_width(), self.get_content_height())
    
    def get_box_x(self) -> int:
        return self.get_x() + self.margin_left

    def get_box_y(self) -> int:
        return self.get_y() + self.margin_top

    def get_relative_x(self) -> int:
        return self.get_box_x() - self.get_parent().padding_left if self.parent else self.get_box_x()
    
    def get_relative_y(self) -> int:
        return self.get_box_y() - self.get_parent().padding_top if self.parent else self.get_box_y()
    
    def get_absolute_x(self) -> int:
        return (self.get_relative_x() + self.get_parent().get_absolute_x()) if self.parent else self.get_box_x()
    
    def get_absolute_y(self) -> int:
        return (self.get_relative_y() + self.get_parent().get_absolute_y()) if self.parent else self.get_box_y()
    

    def get_visual_width(self) -> int:
        return int(self.get_width() * self.get_scale_factor())
    
    def get_visual_height(self) -> int:
        return int(self.get_height() * self.get_scale_factor())
    
    def get_visual_size(self) -> tuple[int, int]:
        return (self.get_visual_width(), self.get_visual_height())
    
    def get_visual_relative_x(self) -> int:
        return int(self.get_relative_x() * self.get_scale_factor())
    
    def get_visual_relative_y(self) -> int:
        return int(self.get_relative_y() * self.get_scale_factor())
    
    def get_visual_absolute_x(self) -> int:
        return int(self.get_absolute_x() * self.get_scale_factor())
    
    def get_visual_absolute_y(self) -> int:
        return int(self.get_absolute_y() * self.get_scale_factor())


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

        IMPORTANT: Parent widgets should call this method of their children to propagate events.
        
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

    
    def draw(self, clip: SurfaceClip) -> None:
        """
        Draw the widget on the given clip.

        Draw order:

        - `draw_expand`: draw something out of the widget's own area, like shadows or something.
        - `draw_self`: draw the widget itself on the given clip
            - `draw_background`
            - `draw_foreground`
                - `draw_content`
                - `draw_children`
            - `draw_border`

        :param clip: a SurfaceClip of the widget's parent to draw on
        :type clip: SurfaceClip
        """
        self.draw_expand(clip)
        self_clip = clip.subclip(Rect(self.get_visual_relative_x(), self.get_visual_relative_y(), self.get_visual_width(), self.get_visual_height()))
        self.draw_self(self_clip)

    def draw_expand(self, clip: SurfaceClip) -> None:
        """
        draw something out of the widget's own area, like shadows or something.
        
        :param self: 说明
        :param clip: 说明
        :type clip: SurfaceClip
        """
        pass

    def draw_self(self, clip: SurfaceClip) -> None:
        """
        Draw the widget itself on the given clip.

        :param clip: a SurfaceClip of the widget itself
        :type clip: SurfaceClip
        """
        self.draw_background(clip)
        self.draw_foreground(clip)
        self.draw_border(clip)

    def draw_background(self, clip: SurfaceClip) -> None:
        """
        Draw the background of the widget on the given clip.

        :param clip: a SurfaceClip of the widget itself
        :type clip: SurfaceClip
        """
        pass

    def draw_foreground(self, clip: SurfaceClip) -> None:
        """
        Draw the foreground of the widget on the given clip.

        :param clip: a SurfaceClip of the widget itself
        :type clip: SurfaceClip
        """
        self.draw_content(clip)
        self.draw_children(clip)

    def draw_content(self, clip: SurfaceClip) -> None:
        """
        Draw the content of the widget on the given clip.

        :param clip: a SurfaceClip of the widget itself
        :type clip: SurfaceClip
        """
        pass

    def draw_children(self, clip: SurfaceClip) -> None:
        """
        Draw the children of the widget on the given clip.

        :param clip: a SurfaceClip of the widget itself to draw children on
        :type clip: SurfaceClip
        """
        for child in self.get_children():
            child.draw(clip) if child.visible else None

    def draw_border(self, clip: SurfaceClip) -> None:
        """
        Draw the border of the widget on the given clip.

        :param clip: a SurfaceClip of the widget itself
        :type clip: SurfaceClip
        """
        pass