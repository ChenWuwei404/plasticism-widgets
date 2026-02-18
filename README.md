# plasticism-widgets

Pygame based widget-lib, with which developers can build GUI by Qt-styled structure and Pygame features.

## Design & Structure

Each plasticism widget is constructed with three parts: event handler, rendering and optional extension functions. Designers can easily combine the abstract classes into one usable class, or even extend them.

### Main Modules

- `core`: basic definitions and system method packages
- `gui`: abstract classes that contain basic UI logic
- `widget`: ready-to-use widgets

## Highlights

### Event Handling

Plasticism provides a stream event processing system, where event processors could be insert. Once a widget received a `Event`, it will be packed into a `EventBundle`, which will be processed by following `EventProcessor`s.

For example, there is a `Button` class with a processor `ButtonStateMachine`, dealing events and generate `ButtonClicked` into the event bundle. As a inheritance of `Button`, `ToggleButton` has a `ToggleStateMachine`, which generate `ToggleOn` or `ToggleOff` when `ButtonClick`ed.

### Customizable

Each method is easy to override for create custom functions and render.

See `plasticism.gui.widget.Widget` for basic definitions of a `Widget`.

## Quick Start

```python
import pygame
from plasticism.gui import Widget, Window
from plasticism.widget import Label

main_widget = Widget()

main_widget.add_child(Label("Hello, World!"))

window = Window((800, 600), main_widget, pygame.RESIZABLE, vsync=1)
window.exec()
```

It will display a window contains "Hello, World!" on the left-top.
