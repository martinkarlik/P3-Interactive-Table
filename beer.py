HISTORY_RING = 10


class Beer:

    def __init__(self, center):
        self.center = center

        self.is_present_current_frame = True
        self.presence_history = [True]

        self.highlighted = False
        self.green_ball = False
        self.red_ball = False
        self.green_buffer = []
        self.red_buffer = []

    def update_history(self, beer_present):

        self.presence_history.append(beer_present)
        if len(self.presence_history) < HISTORY_RING:
            self.presence_history.pop(0)