class Page:
    def __init__(self, s):
        self.screen = s
        self.screen_w = 0
        self.screen_h = 0
        self.players = []
        self.map = None
        self.time = None
    def set_screen_size(self, size):
        self.screen_w, self.screen_h = size
    def update_state(self, state):
        self.players = state['players']
        self.time = state['time']
    def set_map(self, map):
        self.map = map

    #overridden methods
    def handle_keydown(self, key):
        pass
    def handle_keyup(self, key):
        pass
    def handle_mouse_event(self, position):
        pass
    def render(self):
        pass