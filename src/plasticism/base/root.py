from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from plasticism.gui import Window

from plasticism.base import Widget

from plasticism.core.trigger import Trigger
from plasticism.core.assigner import AssignerItem
from plasticism.core.event import Event, Quit

class Root(Widget):
    def __init__(self) -> None:
        super().__init__()
        self.window: Optional['Window'] = None

        self.window_quit = AssignerItem(Quit)
        self.assigner.add_item(self.window_quit)

        self.on_window_quit = Trigger(Quit)
        self.window_quit.connect(self.on_window_quit)

    def set_window(self, window: 'Window') -> None:
        self.window = window
        self.on_window_quit.connect(self.window.exit)

    def get_window(self) -> 'Window':
        if self.window:
            return self.window
        raise ValueError("This Root widget has not been set window.")

    def event_fetch_check(self, event: Event) -> bool:
        return super().event_fetch_check(event) or isinstance(event, Quit)