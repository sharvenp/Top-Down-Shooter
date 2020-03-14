
class Controller:

    def __init__(self, controlled_object):
        self.controlled_object = controlled_object

    def handle(self, event, gui_list):
        raise NotImplementedError