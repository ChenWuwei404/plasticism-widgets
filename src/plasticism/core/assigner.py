from typing import TypeVar, Generic, Type

from plasticism.core.event import Event
from plasticism.core.trigger import Trigger

T = TypeVar("T", bound=Event)

class AssignerItem(Generic[T]):
    def __init__(self, event_type: Type[T]) -> None:
        super().__init__()
        self.event_type: Type[T] = event_type
        self.triggers: list[Trigger[T]] = []

    def check(self, event: Event) -> bool:
        return isinstance(event, self.event_type)
    
    def run(self, event: T) -> None:
        [trigger(event) for trigger in self.triggers]

    def connect(self, trigger: Trigger[T]) -> None:
        self.triggers.append(trigger)

    def disconnect(self, trigger: Trigger[T]) -> None:
        self.triggers.remove(trigger)

    def clear(self) -> None:
        self.triggers.clear()

class Assigner:
    def __init__(self) -> None:
        self.items: list[AssignerItem] = []

    def add_item(self, item: AssignerItem) -> None:
        self.items.append(item)

    def remove_item(self, item: AssignerItem) -> None:
        self.items.remove(item)

    def emit(self, event: Event) -> None:
        for item in self.items:
            if item.check(event):
                item.run(event)