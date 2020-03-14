
from gui_element import GUI_ELEMENT

class Projectile(GUI_ELEMENT):

    def __init__(self):
        GUI_ELEMENT.__init__(self)

    def step(self):
        raise NotImplementedError