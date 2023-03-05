from manim import *
import numpy as np

from mobjects import *
from helperStructures import *

from consts import *


class ForceVisual(Scene):
    def construct(self):
        ax = Axes(
            x_range=X_RANGE,
            y_range=Y_RANGE,
            axis_config={
                "include_ticks": False
            },
            x_length=X_LENGTH,
            y_length=Y_LENGTH
        )
        self.play(Create(ax))

        mainCharge = Charge(Charge.Type.NEGATIVE).move_to(
            ax.c2p(*MAIN_CHARGE_POSITION))
        mainChargeLabel = Tex("-q").next_to(mainCharge, DOWN)
        chargedLine = Line(ax.c2p(*CHARGED_LINE_START), ax.c2p(
            *CHARGED_LINE_END), stroke_width=10, color=RED)
        chargedLineLabel = Tex("Q").next_to(chargedLine, LEFT)
        self.play(DrawBorderThenFill(
            VGroup(mainCharge, chargedLine, mainChargeLabel, chargedLineLabel)))

        self.play(chargedLine.animate.set_color(RED_A).set_stroke_width(5))
        initialDiffCharge = Charge(Charge.Type.POSITIVE).move_to(
            chargedLine.get_center())
        self.play(chargedLineLabel.animate.next_to(
            initialDiffCharge, LEFT).scale(0.7))
        self.play(DrawBorderThenFill(initialDiffCharge))

        initialChargeInfo = ChargeWithInfo(
            initialDiffCharge, chargedLineLabel, mainCharge)
        charges = [initialChargeInfo]
        self.play(Create(initialChargeInfo.forceVector))

        chargeShiftValue = CHARGE_SHIFT_VALUE * UP
        for i in range(1, 1 + NUMBER_OF_APPROXIS):
            newCharges = []
            animationQueue = []
            for charge in charges:
                chargeChangeAnim, old, new = charge.split()
                newCharges += [old, new]
                self.add(new.forceVector)

                animationQueue += [old.charge.animate.shift(-1 * chargeShiftValue).scale(
                    0.7), new.charge.animate.shift(chargeShiftValue).scale(0.7)]
                animationQueue += [old.text.animate.become(
                    Tex(fr"$\frac{{Q}}{{{2**i}}}$").scale(0.7/np.sqrt(i))), new.text.animate.become(
                    Tex(fr"$\frac{{Q}}{{{2**i}}}$").scale(0.7/np.sqrt(i)))]
                animationQueue += chargeChangeAnim

            self.play(*animationQueue, run_time=2)
            charges = newCharges
            chargeShiftValue /= 2
