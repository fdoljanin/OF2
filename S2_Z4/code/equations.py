from manim import *
from consts import *

diffArrayEqn_x = MathTex(r"dF_x",
                         r"& = dF\frac{x}{\sqrt{x^2+L^2}}\\",
                         r"& = k\frac{q \lambda dL}{x^2+L^2}\frac{x}{\sqrt{x^2+L^2}}\\",
                         r"& = kq{\lambda}x\frac{dL}{\sqrt{(x^2+L^2)^3}}\\",
                         font_size=EQ_FONT_SIZE)

intArrayEqn_x = MathTex(r"F_x & = \int", r"dF_x\\",
                        r"& = \int_{0}^{a} kq{\lambda}x\frac{dL}{\sqrt{(x^2+L^2)^3}}\\",
                        r"& = kq{\lambda}x\int_{0}^{a}\frac{dL}{\sqrt{(x^2+L^2)^3}}\\",
                        r"& = kq{\lambda}x\left[\frac{1}{x^2}\frac{L}{\sqrt{L^2+x^2}}\right]_0^a\\",
                        r"& = kq{\lambda}x\frac{1}{x^2}\left(\frac{a}{\sqrt{a^2+x^2}} - 0\right)\\",
                        r"& = kq\frac{ {\lambda}a}{x\sqrt{a^2+x^2}}", r" = \frac{kQq}{x\sqrt{a^2+x^2}}",
                        font_size=EQ_FONT_SIZE)

intExpandEqn_x = MathTex(
    r"\int\frac{dL}{\sqrt{(x ^ 2+L ^ 2) ^ 3}}",
    r"& = \frac{1}{x^3}\int\frac{dL}{\left(1+\frac{L^2}{x^2}\right)^\frac{3}{2}}\\",
    r"""& = \begin{vmatrix}
         \tan\theta = \frac{L}{x}\\
         \frac{1}{\cos^2\theta}d\theta = \frac{dL}{x}
       \end{vmatrix}\\""",
    r"& = \frac{1}{x^3}\int\frac{x}{\cos^2\theta}\frac{d\theta}{\left(1+\tan^2\theta\right)^{\frac{3}{2}}}\\",
    r"& = \frac{x}{x^3}\int\frac{1}{\cos^2\theta}\frac{d\theta}{\left(\frac{1}{\cos^2\theta}\right)^\frac{3}{2}}\\",
    r"& = \frac{1}{x^2}\int\cos\theta{d}\theta\\",
    r"& = \frac{1}{x^2}\sin\theta + C\\",
    r"& = \frac{1}{x^2}\sin\tan^{-1}\left(\frac{L}{x}\right) + C\\",
    r"& = \frac{1}{x^2}\frac{L}{\sqrt{L^2+x^2}} + C",
    font_size=EQ_FONT_SIZE)

forceResult_x = MathTex(
    r"F_x = \frac{kQq}{x\sqrt{a^2+x^2}}", font_size=EQ_FONT_SIZE)

forceResult_y = MathTex(
    r"F_y = \frac{kqQ}{a}\left(\frac{1}{x} - \frac{1}{\sqrt{x^2+a^2}}\right)", font_size=EQ_FONT_SIZE)

intArrayEqn_y = MathTex(r"F_y & = {\int}dF\frac{L}{\sqrt{x^2+L^2}}\\",
                        r"& = \int_{0}^{a}k\frac{q{\lambda}dL}{x^2+L^2}\frac{L}{\sqrt{x^2+L^2}}\\",
                        r"& = kq{\lambda}\int_{0}^{a}\frac{L dL}{\left(x^2+L^2\right)^\frac{3}{2}}\\",
                        r"& = kq{\lambda}\left[-\frac{1}{\sqrt{x^2+L^2}}\right]_{0}^{a}\\",
                        r"& = \frac{kqQ}{a}\left(\frac{1}{x} - \frac{1}{\sqrt{x^2+a^2}}\right)",
                        font_size=EQ_FONT_SIZE)
intExpandEqn_y = MathTex(r"\int\frac{L dL}{\left(x^2+L^2\right)^\frac{3}{2}}",
                         r"""& = \begin{vmatrix}
                                     u = x^2+L^2 \\
                                     du = 2LdL
                                   \end{vmatrix}\\""",
                         r"& = \frac{1}{2}\int\frac{du}{u^\frac{3}{2}}\\",
                         r"& = -\frac{1}{2\cdot\frac{1}{2}}u^{-\frac{1}{2}} + C\\",
                         r"& = -\frac{1}{\sqrt{x^2+L^2}} + C",
                         font_size=EQ_FONT_SIZE)
