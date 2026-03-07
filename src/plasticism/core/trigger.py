from typing import Callable, TypeVar, Generic, Type, Union

from plasticism.core.event import Event

import inspect

T = TypeVar("T", bound=Event)

TriggerAction = Union[Callable[[], None], Callable[[T], None]]

class Trigger(Generic[T]):
    def __init__(self, event_type: Type[T]) -> None:
        self.actions: list[TriggerAction] = []
        self.event_type: Type[T] = event_type

    def connect(self, action: TriggerAction) -> None:
        self.actions.append(action)

    def disconnect(self, action: TriggerAction) -> None:
        self.actions.remove(action)
    
    def clear(self) -> None:
        self.actions.clear()

    def emit(self, event: T) -> None:
        for action in self.actions:
            action(event) if len(inspect.signature(action).parameters) else action()  # type: ignore

    def __call__(self, event: T) -> None:
        self.emit(event)