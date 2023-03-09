from manim import *
import numpy as np

from mobjects import *
from helperStructures import *

from helpers import getCoulombForce
from consts import *
from equations import *

from manim_slides import Slide  # I changed its base class to MovingCameraScene


class ForceVisual(Slide):
    def construct(self):
        titleMobject = Tex(r"2. seminar - 4. zadatak")
        self.play(Create(titleMobject))
        self.wait()
        self.pause()

        self.play(Uncreate(titleMobject))
        self.remove(titleMobject)

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
        self.pause()

        self.play(chargedLine.animate.set_color(RED_A).set_stroke_width(5))
        initialDiffCharge = Charge(Charge.Type.POSITIVE).move_to(
            chargedLine.get_center())
        self.play(chargedLineLabel.animate.scale(0.7))
        self.play(DrawBorderThenFill(initialDiffCharge), chargedLineLabel.animate.next_to(
            initialDiffCharge, LEFT*0.7))

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
            if i <= 2:
                self.pause()

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
        self.pause()

        toBeFaded = []
        observedDiff = charges[OBSERVED_DIFF_INDEX]
        for chargeInfo in charges:
            if chargeInfo != observedDiff:
                toBeFaded += [chargeInfo.charge,
                              chargeInfo.text, chargeInfo.forceVector]
        self.play(FadeOut(VGroup(*toBeFaded)))
        self.play(observedDiff.text.animate.become(Tex("dQ").scale(0.5)))

        # optimization
        observedDiff.stopUpdaters()
        for chargeInfo in charges:
            if chargeInfo != observedDiff:
                self.remove(chargeInfo)

        self.camera.frame.save_state()
        observedDiffLabel = Tex(r"$d\vec{F}$").scale(
            0.2).align_to(observedDiff.forceVector, UP+RIGHT).shift(UP*0.05)
        self.play(self.camera.frame.animate.scale(
            CAMERA_ZOOM_1).move_to(observedDiff.forceVector), Create(observedDiffLabel))
        self.pause()
        self.play(Restore(self.camera.frame))

        self.play(FadeOut(VGroup(totalForceDescription, totalForceVector)))
        self.remove(totalForceDescription, totalForceVector)
        diffCopy = observedDiff.forceVector.copy()
        zoomedDiffVector = Vector(
            VECTOR_DIFF_ZOOM*observedDiff.forceVector.get_vector()).move_to(RIGHT+UP*2).set_color(PURPLE_C)
        self.play(diffCopy.animate.become(zoomedDiffVector), run_time=3)
        zoomedDiffLabel = Tex(r"$d\vec{F}$").scale(FORCE_LABEL_SIZE).move_to(
            zoomedDiffVector.get_center()+0.1*DL, aligned_edge=UR).set_color(PURPLE_C)
        self.play(Create(zoomedDiffLabel))
        self.pause()

        diff_x, diff_y = getVectorComponents(zoomedDiffVector)
        self.play(Create(VGroup(diff_x, diff_y)))
        self.play(diff_x.animate.shift(UP*zoomedDiffVector.get_vector()[1]))
        diffLabel_x = Tex(r"$dF_x$").scale(
            FORCE_LABEL_SIZE).move_to(diff_x.get_top(), aligned_edge=DOWN)
        diffLabel_y = Tex(r"$dF_y$").scale(
            FORCE_LABEL_SIZE).move_to(diff_y.get_right(), aligned_edge=LEFT)
        self.play(Create(VGroup(diffLabel_x, diffLabel_y)))
        self.pause()

        coulombEq = MathTex(
            r"d\vec{F_q}", r"= k\frac{q \cdot dQ}{r_{12}^2}\hat{r}_{21}", font_size=EQ_FONT_SIZE)
        coulombEq[0][1:4].set_color(PURPLE_C)  # F_q
        coulombEq[1][2:3].set_color(BLUE)  # q
        coulombEq[1][4:6].set_color(RED)  # dQ
        self.play(Write(coulombEq), mainChargeLabel.animate.set_color(
            BLUE), observedDiff.text.animate.set_color(RED), run_time=2)
        self.pause()

        coulombEqExpand = MathTex(
            r"= k\frac{q\cdot \lambda dL}{r_{12}^2}\hat{r}_{21}", font_size=EQ_FONT_SIZE).next_to(coulombEq, RIGHT)
        self.play(Write(coulombEqExpand))
        self.pause()

        mainChargeBrace = BraceBetweenPoints(
            ax.get_origin(), mainCharge.get_center())
        mainChargeBraceText = mainChargeBrace.get_text("x")
        diffChargeBrace = BraceBetweenPoints(
            ax.get_origin(), observedDiff.charge.get_center(), direction=LEFT)
        diffChargeBraceText = diffChargeBrace.get_text("L")
        self.play(Create(VGroup(mainChargeBrace, mainChargeBraceText)))
        self.play(Create(VGroup(diffChargeBrace, diffChargeBraceText)))
        self.pause()

        coulombEqUpdate = MathTex(
            r"= k\frac{q\cdot \lambda dL}{x^2+L^2}\hat{r}_{21}", font_size=EQ_FONT_SIZE).next_to(coulombEq, RIGHT)
        self.play(coulombEqExpand.animate.become(
            coulombEqUpdate), run_time=2)
        self.pause()

        coulombEq_x = MathTex(
            r"dF_x = dF\frac{x}{\sqrt{x^2+L^2}}", font_size=EQ_FONT_SIZE).next_to(coulombEq, DOWN).align_to(coulombEq, LEFT)
        coulombEq_y = MathTex(
            r"dF_y = dF\frac{L}{\sqrt{x^2+L^2}}", font_size=EQ_FONT_SIZE).next_to(coulombEq_x, RIGHT)
        self.play(Write(coulombEq_x), run_time=2)
        self.play(Write(coulombEq_y), run_time=2)
        self.pause()

        # integration_X
        gc = []
        animationQueue = []
        integrationTitle_x = Tex("Integracija za $x$").move_to(5*DOWN+5*LEFT)
        diffArrayEqn_x.next_to(integrationTitle_x, DOWN).align_to(
            integrationTitle_x, LEFT)

        cEq_copy = coulombEq_x.copy()
        animationQueue += [Create(integrationTitle_x),
                           cEq_copy.animate.become(diffArrayEqn_x[0:2])]
        animationQueue += [self.camera.frame.animate.shift(8*DOWN)]
        self.play(*animationQueue, run_time=5)
        self.pause()

        animationQueue = getMultipartTexMorphAnimation(
            diffArrayEqn_x, start=2, garbageCollector=gc)
        for anim in animationQueue:
            self.play(anim)
            self.pause()

        intArrayEqn_x.next_to(diffArrayEqn_x).shift(
            4*RIGHT).align_to(diffArrayEqn_x, UP)
        self.play(Create(intArrayEqn_x[0]))
        dAE_copy = diffArrayEqn_x[0].copy()
        self.play(dAE_copy.animate.become(intArrayEqn_x[1]))
        self.pause()

        animationQueue = getMultipartTexMorphAnimation(
            intArrayEqn_x, start=2, end=3, garbageCollector=gc)
        for anim in animationQueue:
            self.play(anim)
            self.pause()

        # integrate F_x till end
        self.camera.frame.save_state()
        intExpandEqn_x.next_to(intArrayEqn_x, RIGHT).shift(
            2*RIGHT).align_to(intArrayEqn_x, UP)
        animationQueue = []
        iAE_copy = intArrayEqn_x[3].copy()
        animationQueue += [iAE_copy.animate.become(intExpandEqn_x[0])]
        animationQueue += [self.camera.frame.animate.shift(RIGHT*8+DOWN)]
        self.play(*animationQueue)
        self.pause()

        animationQueue = getMultipartTexMorphAnimation(
            intExpandEqn_x, start=1, garbageCollector=gc)
        for anim in animationQueue:
            self.play(anim)
            self.pause()

        animationQueue = []
        animationQueue += [intExpandEqn_x[-1].animate.become(intArrayEqn_x[4])]
        animationQueue += [Restore(self.camera.frame)]
        self.play(*animationQueue, run_time=2)
        self.pause()

        animationQueue = getMultipartTexMorphAnimation(
            intArrayEqn_x, start=5, garbageCollector=gc)
        for anim in animationQueue:
            self.play(anim)
            self.pause()

        forceSurroundRectange_x = SurroundingRectangle(
            intArrayEqn_x[-1], color=PURPLE_C)
        self.play(Create(forceSurroundRectange_x), run_time=2)

        # move to origin
        animationQueue = []
        forceResult_x.next_to(coulombEq_x, DOWN).align_to(coulombEq_x, LEFT)
        self.play(self.camera.frame.animate.scale(CAMERA_ZOOM_2), run_time=2)
        animationQueue += [intArrayEqn_x[-1].copy().animate.become(forceResult_x)]
        animationQueue += [self.camera.frame.animate.scale(
            1/CAMERA_ZOOM_2).move_to(ORIGIN)]
        self.play(*animationQueue, run_time=2)
        self.pause()

        # optimization
        gc += [dAE_copy, iAE_copy, integrationTitle_x, cEq_copy]
        self.remove(*gc)

        self.camera.frame.save_state()
        # start y anim
        animationQueue = []
        integrationTitle_y = Tex(
            "Integracija za $y$").move_to(3*UP + 9.2*RIGHT)
        intArrayEqn_y.next_to(integrationTitle_y, DOWN).align_to(
            integrationTitle_y, LEFT)

        animationQueue += [Create(integrationTitle_y),
                           coulombEq_y.copy().animate.become(intArrayEqn_y[0])]
        animationQueue += [self.camera.frame.animate.shift(14.2*RIGHT)]
        self.play(*animationQueue)
        self.wait()
        self.pause()
        # integrate y
        animationQueue = getMultipartTexMorphAnimation(
            intArrayEqn_y, start=1, end=2)
        for anim in animationQueue:
            self.play(anim)
            self.pause()

        intExpandEqn_y.next_to(intArrayEqn_y, RIGHT).shift(
            2*RIGHT).align_to(intArrayEqn_y, UP)
        self.play(intArrayEqn_y[2].animate.become(intExpandEqn_y[0]))
        self.pause()

        animationQueue = getMultipartTexMorphAnimation(intExpandEqn_y, start=1)
        for anim in animationQueue:
            self.play(anim)
            self.pause()

        self.play(intExpandEqn_y[-1].animate.become(intArrayEqn_y[3]))
        self.pause()
        animationQueue = getMultipartTexMorphAnimation(intArrayEqn_y, start=4)
        for anim in animationQueue:
            self.play(anim)
            self.pause()

        forceSurroundRectange_y = SurroundingRectangle(
            intArrayEqn_y[-1], color=PURPLE_C)
        self.play(Create(forceSurroundRectange_y), run_time=2)

        # move to origin
        animationQueue = []
        forceResult_y.next_to(coulombEq_y, DOWN).align_to(coulombEq_y, LEFT)
        self.play(self.camera.frame.animate.scale(CAMERA_ZOOM_2), run_time=2)
        animationQueue += [intArrayEqn_y[-1].copy().animate.become(forceResult_y)]
        animationQueue += [Restore(self.camera.frame)]
        self.play(*animationQueue, run_time=2)
        self.pause()
        self.play(self.camera.frame.animate.shift(8*LEFT))


class ForceDemo(Slide):
    def construct(self):
        self.camera.frame.save_state()
        self.camera.frame.shift(7*RIGHT)

        ax = Axes(axis_config={
            "include_ticks": False
        })
        self.play(Create(ax), Restore(self.camera.frame))

        chargedLineLength = DEMO_LINELEN_1
        mainCharge = Charge(Charge.Type.NEGATIVE).move_to(
            MAIN_CHARGE_POSITION_DEMO).scale(0.7)
        mainChargeLabel = Tex("-q").next_to(mainCharge, DOWN)
        chargedLine = Line([0, 0, 0], [0, chargedLineLength,
                           0], stroke_width=8, color=RED)
        chargedLineLabel = Tex("Q").next_to(chargedLine, LEFT)
        self.play(DrawBorderThenFill(
            VGroup(mainCharge, chargedLine, mainChargeLabel, chargedLineLabel)))
        self.wait()

        self.play(FadeOut(VGroup(mainChargeLabel, chargedLineLabel)))
        self.remove(mainChargeLabel, chargedLineLabel)

        self.play(Create(fieldEqn.shift(UP*2+RIGHT*3)), run_time=4)
        self.wait()
        self.pause()

        self.play(Uncreate(fieldEqn))
        self.remove(fieldEqn)

        forceVector = always_redraw(lambda: Arrow(start=mainCharge.get_center(
        ), end=mainCharge.get_center()+getFieldVectorFromTask(chargedLineLength, DEMO_CHARGE_ON_LINE, mainCharge), buff=SMALL_BUFF))
        self.play(Create(forceVector))
        self.pause()

        self.start_loop()
        for position in DEMO_POSITIONS:
            self.play(mainCharge.animate.move_to(position))
        self.end_loop()

        self.start_loop()
        self.play(Rotating(mainCharge,
                           radians=2 * PI,
                           about_point=ORIGIN), run_time=6)
        self.end_loop()

        self.play(FadeOut(VGroup(forceVector, mainCharge)))

        forceVector.clear_updaters()
        self.remove(forceVector, mainCharge)
        self.pause()

        chargedLineLength = ValueTracker(DEMO_LINELEN_1)

        def fieldFunc(pos): return np.array(
            getFieldVectorFromTask(chargedLineLength.get_value(), DEMO_CHARGE_ON_LINE, position=pos))

        forceField = always_redraw(lambda: ArrowVectorField(fieldFunc))
        self.play(*[GrowArrow(force) for force in forceField], run_time=2)
        self.add(forceField)
        self.wait()
        self.pause()

        chargedLine.add_updater(lambda cl: cl.put_start_and_end_on(
            [0, 0, 0], [0, chargedLineLength.get_value(), 0]))

        self.play(chargedLineLength.animate.set_value(
            DEMO_LINELEN_2))
        self.wait()
        self.pause()
        self.play(chargedLineLength.animate.set_value(
            DEMO_LINELEN_3), run_time=2)
        self.wait()
        self.pause()
        self.wait()
