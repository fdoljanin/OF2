from manim import *


class ChargeWithInfo():
    def getUpdatedVector(self):
        posX = 0.5 / (self.mainCharge.get_center()
                      [0] - self.charge.get_center()[0])
        posY = 0.5 / (self.mainCharge.get_center()
                      [1] - self.charge.get_center()[1])
        return Vector([posX, posY]).next_to(self.charge, RIGHT*2)

    def __init__(self, charge, text, mainCharge):
        self.charge = charge
        self.text = text
        self.mainCharge = mainCharge

        text.clear_updaters()
        text.add_updater(lambda x: x.next_to(charge, LEFT))
        self.forceVector = always_redraw(self.getUpdatedVector)

    def copy(self):
        return ChargeWithInfo(self.charge.copy(), self.text.copy(), self.mainCharge)
