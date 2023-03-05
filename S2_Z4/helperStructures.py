from manim import *


class ChargeWithInfo():
    def getUpdatedVector(self):
        posX = self.charge.amount.get_value()
        posY = self.charge.amount.get_value()
        return Vector([posX, posY]).next_to(self.charge, RIGHT*2)

    def __init__(self, charge, text, mainCharge):
        self.charge = charge
        self.text = text
        self.mainCharge = mainCharge

        text.clear_updaters()
        text.add_updater(lambda x: x.next_to(charge, LEFT))
        self.forceVector = always_redraw(self.getUpdatedVector)

    def split(self):
        copy = ChargeWithInfo(self.charge.copy(),
                              self.text.copy(), self.mainCharge)

        chargeChangeAnim = []
        chargeChangeAnim += [self.charge.amount.animate.set_value(
            self.charge.amount.get_value() / 2)]
        chargeChangeAnim += [copy.charge.amount.animate.set_value(
            copy.charge.amount.get_value() / 2)]

        return (chargeChangeAnim, self, copy)
