from manim import *
from helpers import *


class ChargeWithInfo():
    def getUpdatedVector(self):
        force = getCoulombForce(self.mainCharge, self.charge)

        return Vector(force).next_to(self.charge, RIGHT+DOWN*0.5, aligned_edge=UP+LEFT)

    def __init__(self, charge, text, mainCharge):
        self.charge = charge
        self.text = text
        self.mainCharge = mainCharge

        text.clear_updaters()
        text.add_updater(lambda x: x.next_to(charge, LEFT*0.7))
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


def getMultipartTexMorphAnimation(texMobject, start=0, end=0, garbageCollector=[]):
    end = end if end > 0 else len(texMobject)-1

    animationQueue = []
    if start == 0:
        animationQueue += [Write(texMobject[0])]
        prev = texMobject[0].copy()
    else:
        prev = texMobject[start-1].copy()

    garbageCollector += [prev]

    for i in range(start, end+1):
        new = texMobject[i]
        animationQueue += [prev.animate.become(new)]
        prev = new.copy()

        garbageCollector += [prev]

    return animationQueue
