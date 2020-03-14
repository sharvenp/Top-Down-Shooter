
from gui_element import GUI_ELEMENT

class Controllable(GUI_ELEMENT):

    def __init__(self):
        GUI_ELEMENT.__init__(self)

    def attach_controller(self, controller):
        self.controller = controller