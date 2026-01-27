from plasticism.core.transition import State, Transition, Machine
from plasticism.core.transition import class_judger

from plasticism.gui.widget import MouseEnter, MouseLeave
from plasticism.core.event import MousePress, MouseRelease, LocalEvent, MouseEvent, MouseButton

class ButtonClick(LocalEvent, MouseButton):
    pass

class ButtonMachine(Machine):
    def __init__(self) -> None:
        super().__init__()
        self.idle = State("idle")
        self.hover = State("hover")
        self.pressed = State("pressed")

        self.idle.add_transition(Transition(
            self.hover,
            class_judger(MouseEnter),
        ))

        self.hover.add_transition(Transition(
            self.idle,
            class_judger(MouseLeave),
        ))

        self.hover.add_transition(Transition(
            self.pressed,
            class_judger(MousePress),
        ))

        self.pressed.add_transition(Transition[MouseRelease](
            self.hover,
            class_judger(MouseRelease),
            lambda e: ButtonClick(e.x, e.y, e.button),
        ))

        self.pressed.add_transition(Transition(
            self.idle,
            class_judger(MouseLeave)
        ))

        self.add_states([self.idle, self.hover, self.pressed])
        self.set_current_state(self.idle)