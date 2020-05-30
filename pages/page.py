class Page:
    def __init__(self, s):
        self.screen = s
        self.screen_w = 0
        self.screen_h = 0
    def set_screen_size(self, size):
        self.screen_w, self.screen_h = size

    #overridden methods
    def handle_keydown(self, key):
        pass
    def handle_mouse_event(self, position):
        pass
    def render(self):
        pass