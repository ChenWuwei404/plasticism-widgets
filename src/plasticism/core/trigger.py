from typing import Callable, TypeVar, Generic, Type

from plasticism.core.event import Event

T = TypeVar("T", bound=Event)

class Trigger(Generic[T]):
    def __init__(self, event_type: Type[T]) -> None:
        self.actions: list[Callable[[T], None]] = []
        self.event_type: Type[T] = event_type

    def connect(self, action: Callable[[T], None]) -> None:
        self.actions.append(action)

    def disconnect(self, action: Callable[[T], None]) -> None:
        self.actions.remove(action)
    
    def clear(self) -> None:
        self.actions.clear()

    def emit(self, event: T) -> None:
        for action in self.actions:
            action(event)

    def __call__(self, event: T) -> None:
        self.emit(event)