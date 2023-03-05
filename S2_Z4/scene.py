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
        self.play(Create(VGroup(totalForceVector, totalForceDescription)))

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

        self.camera.frame.save_state()
        observedDiffLabel = Tex(r"$d\vec{F}$").scale(
            0.2).align_to(observedDiff.forceVector, UP+RIGHT).shift(UP*0.05)
        self.play(self.camera.frame.animate.scale(
            CAMERA_ZOOM_1).move_to(observedDiff.forceVector), Create(observedDiffLabel))
        self.wait()
        self.play(Restore(self.camera.frame))

        self.play(FadeOut(VGroup(totalForceDescription, totalForceVector)))
        diffCopy = observedDiff.forceVector.copy()
        zoomedDiffVector = Vector(
            VECTOR_DIFF_ZOOM*observedDiff.forceVector.get_vector()).move_to(RIGHT+UP*2).set_color(PURPLE_C)
        self.play(diffCopy.animate.become(zoomedDiffVector), run_time=3)
        zoomedDiffLabel = Tex(r"$d\vec{F}$").scale(FORCE_LABEL_SIZE).move_to(
            zoomedDiffVector.get_center()+0.1*DL, aligned_edge=UR).set_color(PURPLE_C)
        self.play(Create(zoomedDiffLabel))

        diff_x, diff_y = getVectorComponents(zoomedDiffVector)
        self.play(Create(VGroup(diff_x, diff_y)))
        self.play(diff_y.animate.shift(RIGHT*zoomedDiffVector.get_vector()[0]))
        diffLabel_x = Tex(r"$dF_x$").scale(
            FORCE_LABEL_SIZE).move_to(diff_x.get_top(), aligned_edge=DOWN)
        diffLabel_y = Tex(r"$dF_y$").scale(
            FORCE_LABEL_SIZE).move_to(diff_y.get_right(), aligned_edge=LEFT)
        self.play(Create(VGroup(diffLabel_x, diffLabel_y)))

        coulombEq = MathTex(
            r"d\vec{F_q}", r"= k\frac{q \cdot dQ}{r_{12}^2}\hat{r}_{21}", font_size=EQ_FONT_SIZE)
        coulombEq[0][1:4].set_color(PURPLE_C)  # F_q
        coulombEq[1][2:3].set_color(BLUE)  # q
        coulombEq[1][4:6].set_color(RED)  # dQ
        self.play(Write(coulombEq), mainChargeLabel.animate.set_color(
            BLUE), observedDiff.text.animate.set_color(RED), run_time=2)
        coulombEqDensity = MathTex(
            r"= k\frac{q\cdot \lambda dL}{r_{12}^2}\hat{r}_{21}", font_size=EQ_FONT_SIZE).next_to(coulombEq, RIGHT)
        self.play(Write(coulombEqDensity))

        mainChargeBrace = Brace(Line(ax.get_origin(), mainCharge.get_center()))
        mainChargeBraceText = mainChargeBrace.get_text("x")
        diffChargeBrace = Brace(
            Line(ax.get_origin(), observedDiff.charge.get_center()), direction=UP)
        diffChargeBraceText = diffChargeBrace.get_text("L")
        self.play(Create(VGroup(mainChargeBrace, mainChargeBraceText)))
        self.play(Create(VGroup(diffChargeBrace, diffChargeBraceText)))
