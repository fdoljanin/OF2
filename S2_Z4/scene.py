from manim import *
import numpy as np

from mobjects import *
from helperStructures import *

from helpers import getCoulombForce
from consts import *


class ForceVisual(MovingCameraScene):
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
        totalForceDescription = Tex(r"$\sum_{i}^{} \vec{F_i}$").scale(
            0.5).next_to(mainCharge, UP*0.7)
        totalForceVector = Vector(getCoulombForce(
            mainCharge, initialDiffCharge)).next_to(totalForceDescription, UP*0.9)
        self.play(Create(totalForceVector), Write(totalForceDescription))

        chargeShiftValue = CHARGE_SHIFT_VALUE * UP
        for i in range(1, 1 + NUMBER_OF_APPROXIS):
            newCharges = []
            toBeFaded = []
            for chargeInfo in charges:
                chargeChangeAnim, old, new = chargeInfo.split()
                newCharges += [old, new]
                self.add(new.forceVector)

                toBeFaded += [old.charge.animate.shift(-1 * chargeShiftValue).scale(
                    0.7), new.charge.animate.shift(chargeShiftValue).scale(0.7)]
                toBeFaded += [old.text.animate.become(
                    Tex(fr"$\frac{{Q}}{{{2**i}}}$").scale(0.7/np.sqrt(i))), new.text.animate.become(
                    Tex(fr"$\frac{{Q}}{{{2**i}}}$").scale(0.7/np.sqrt(i)))]
                toBeFaded += chargeChangeAnim

            self.play(*toBeFaded, run_time=2)
            charges = newCharges
            chargeShiftValue /= 2

            totalForce = np.add.reduce([charge.forceVector.get_vector()
                                        for charge in charges])
            self.play(totalForceVector.animate.become(
                Vector(totalForce).next_to(mainCharge, UP)))

        toBeFaded = []
        observedDiff = charges[OBSERVED_DIFF_INDEX]
        for chargeInfo in charges:
            if chargeInfo != observedDiff:
                toBeFaded += [chargeInfo.charge,
                              chargeInfo.text, chargeInfo.forceVector]
        self.play(FadeOut(VGroup(*toBeFaded)))
        self.play(observedDiff.text.animate.become(Tex("dQ").scale(0.5)))

        self.play(self.camera.frame.animate.scale(
            CAMERA_ZOOM).move_to(observedDiff.forceVector))
