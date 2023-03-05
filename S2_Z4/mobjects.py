from manim import *


class Charge(Circle):
    class Type(Enum):
        POSITIVE = 0
        NEGATIVE = 1

    def __init__(self, type=Type.POSITIVE, **kwargs):
        CONFIG = {
            "radius": 0.2,
            "stroke_width": 3,
            "color": RED if type == self.Type.POSITIVE else BLUE,
            "fill_opacity": 0.7,
        }
        Circle.__init__(self, **CONFIG, **kwargs)

        plus = Tex("+" if type == self.Type.POSITIVE else "-")
        plus.scale(0.8)
        plus.move_to(self)
        self.add(plus)
