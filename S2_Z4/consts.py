X_RANGE = [0, 10]
Y_RANGE = [0, 10]
X_LENGTH = 10
Y_LENGTH = 6

CHARGED_LINE_LENGTH = 0.8
CHARGED_LINE_START = (X_RANGE[0], Y_RANGE[0], 0)
CHARGED_LINE_END = (X_RANGE[0], Y_RANGE[0] + CHARGED_LINE_LENGTH*Y_RANGE[1], 0)
MAIN_CHARGE_POSITION = (X_RANGE[0] + 0.75*X_RANGE[1], Y_RANGE[0], 0)

CHARGE_SHIFT_VALUE = Y_LENGTH * CHARGED_LINE_LENGTH / 4
NUMBER_OF_APPROXIS = 3
