from plasticism.gui import Window
from plasticism.base import BackgroundBase, RootBase
from plasticism.widget import Widget, Label, FixedScaleLabel

from plasticism.core.layout import AlignHorizontal

from pygame import RESIZABLE

class Main(BackgroundBase, RootBase):
    def get_background_color(self):
        return (0, 0, 0)
    
    def __init__(self) -> None:
        super().__init__()
        self.label1 = Label("This is a Label")
        self.label1.set_x(10)
        self.label1.set_y(10)
        self.label1.set_width(-1)
        self.label1.set_text_align_horizontal(AlignHorizontal.CENTER)

        self.label2 = FixedScaleLabel("Another Label, but will not scale with DPI")
        self.label2.set_x(10)
        self.label2.set_y(50)
        self.label2.set_width(-1)
        self.label2.set_text_align_horizontal(AlignHorizontal.CENTER)

        self.add_child(self.label1)
        self.add_child(self.label2)

root = Main()

window = Window((1280, 720), root, RESIZABLE)

window.exec()