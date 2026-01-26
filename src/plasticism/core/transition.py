from typing import Callable, Optional, Collection
from plasticism.core.event import Event, EventBundle, Processor

from dataclasses import dataclass

class State:
    def __init__(self, name: Optional[str] = None) -> None:
        self.transitions: list['Transition'] = []
        self.name: Optional[str] = name

    def add_transition(self, transition: 'Transition') -> None:
        self.transitions.append(transition)

    def __repr__(self) -> str:
        return f"<State object: {self.name}>" if self.name else f"<State object at {id(self)}>"

@dataclass
class Transition:
    to_state: State
    judger: Callable[[Event], bool]
    signal: Optional[Callable[[Event], Event]] = None

def class_judger(event_class: type[Event]) -> Callable[[Event], bool]:
    return lambda event: isinstance(event, event_class)

class Machine(Processor):
    def __init__(self) -> None:
        self.states: set[State] = set()
        self.current_state: Optional[State] = None

    def add_state(self, state: State) -> None:
        self.states.add(state)
        if self.current_state is None:
            self.current_state = state

    def add_states(self, states: Collection[State]) -> None:
        self.states.update(states)

    def set_current_state(self, state: State) -> None:
        self.current_state = state

    def get_current_state(self) -> State:
        if self.current_state is None:
            raise ValueError("Current state is not set.")
        return self.current_state

    def process_event(self, event_bundle: EventBundle) -> None:
        current_state = self.get_current_state()
        for transition in current_state.transitions:
            for event in event_bundle:
                if transition.judger(event):
                    if transition.signal:
                        event_bundle.append(transition.signal(event))
                    self.set_current_state(transition.to_state)
                    break
