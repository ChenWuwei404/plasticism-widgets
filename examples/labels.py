from plasticism.gui import Window, Widget
from plasticism.widget import Label, FixedScaleLabel

root = Widget()

lable1 = Label("This is a Label")
lable1.set_x(10)
lable1.set_y(10)

label2 = FixedScaleLabel("Another Label, but will not scale with DPI")
label2.set_x(10)
label2.set_y(50)

root.add_child(lable1)
root.add_child(label2)

window = Window((1280, 720), root)

window.exec()