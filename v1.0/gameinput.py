from directkeys import PressKey, ReleaseKey, W, A, S, D
import time


def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    # ReleaseKey(W)


def left():
    PressKey(A)
    ReleaseKey(W)
    ReleaseKey(D)
    # ReleaseKey(A)
    PressKey(W)


def right():
    PressKey(D)
    ReleaseKey(W)
    ReleaseKey(A)
    # ReleaseKey(D)
    PressKey(W)


def slow():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


def drive_with_lane_detection(m1, m2):
    if m1 < 0 and m2 < 0:
        right()
    elif m1 > 0 and m2 > 0:
        left()
    else:
        straight()
