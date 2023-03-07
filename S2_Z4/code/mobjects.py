from manim import *
from enum import IntEnum


class Charge(Circle):
    class Type(IntEnum):
        NEGATIVE = -1
        POSITIVE = 1

    def __init__(self, amount, **kwargs):
        CONFIG = {
            "radius": 0.2,
            "stroke_width": 3,
            "color": RED if amount > 0 else BLUE,
            "fill_opacity": 0.7,
        }
        Circle.__init__(self, **CONFIG, **kwargs)
        self.amount = amount if type(
            amount) == ValueTracker else ValueTracker(amount)

        plus = Tex("+" if amount > 0 else "-")
        plus.scale(0.8)
        plus.move_to(self)
        self.add(plus)
