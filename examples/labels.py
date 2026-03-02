from plasticism.gui import Window
from plasticism.widget import Widget, Label, FixedScaleLabel

from plasticism.core.layout import AlignHorizontal

root = Widget()

label1 = Label("This is a Label")
label1.set_x(10)
label1.set_y(10)
label1.set_width(-1)
label1.set_text_align_horizontal(AlignHorizontal.CENTER)

label2 = FixedScaleLabel("Another Label, but will not scale with DPI")
label2.set_x(10)
label2.set_y(50)
label2.set_width(-1)
label2.set_text_align_horizontal(AlignHorizontal.CENTER)

root.add_child(label1)
root.add_child(label2)

window = Window((1280, 720), root)

window.exec()