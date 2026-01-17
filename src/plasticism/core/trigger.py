from typing import Callable, Optional, TypeVar, Generic

from plasticism.core.event import Event

T = TypeVar("T", bound=Event)

class Trigger(Generic[T]):
    def __init__(self) -> None:
        self.actions: list[Callable[[Optional[T]], None]] = []

    def connect(self, action: Callable[[Optional[T]], None]) -> None:
        self.actions.append(action)

    def disconnect(self, action: Callable[[Optional[T]], None]) -> None:
        self.actions.remove(action)
    
    def clear(self) -> None:
        self.actions.clear()

    def emit(self, event: Optional[T]) -> None:
        for action in self.actions:
            action(event)

    def __call__(self, event: Optional[T]) -> None:
        self.emit(event)