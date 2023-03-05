from manim import *
import numpy as np
from mobjects import *
from consts import *


def getDistance(d1, d2):
    return np.sqrt(np.sum([np.square(d1[i] - d2[i]) for i in range(len(d1))]))


def getCoulombForce(observedCharge: Charge, otherCharge: Charge):
    """Force on observed charge; Coulomb constant is set up for this animation to be well displayed. Returns a 3d vector.

    Parameters
    ----------
    observedCharge
        charge which we are looking at
    otherCharges
        charges which are interacting with observed one"""
    c1, c2 = observedCharge.get_center(), otherCharge.get_center()
    chargeDistance = getDistance(c1, c2)

    forceValue = COULOMB_CONST * observedCharge.amount.get_value(
    ) * otherCharge.amount.get_value() / np.square(chargeDistance)

    valuesPerDimension = [
        forceValue * (c2[i]-c1[i]) / chargeDistance for i in range(len(c1))]

    return valuesPerDimension


def getVectorComponents(observedVector: Vector):
    """"Returns vector components for each dimension."""
    start, end = observedVector.get_start_and_end()
    vector_x = Vector().put_start_and_end_on(
        [start[0], start[1], 0], [end[0], start[1], 0])
    vector_y = Vector().put_start_and_end_on(
        [start[0], start[1], 0], [start[0], end[1], 0])

    return (vector_x, vector_y)