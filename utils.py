import cv2
import numpy as np
import scipy.interpolate

def createCurveFunc(points):
    """ Return a function derived from control points. """

    if points is None:
        return None

    numPoints = len(points)
    if numPoints < 2:
        return None

    xs, ys = zip(*points)
    if numPoints < 4:
        kind = 'linear'
        # 'quadratic' is not implemented

    else:
        kind = 'cubic'

    return scipy.interpolate(xs, ys, kind, bounds_error=False)