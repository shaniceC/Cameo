import cv2
import numpy as np
import utils

def recolorRC(src, dst):
    """ Simulate conversion from BGR to RC (red, cyan).

        The source and destination images must both be in BGR format.
        Blues and greens are replaced with cyans.

        Pseudocode:
        dst.b = dst.g = 0.5 * (src.b + src.g)
        dst.r = src.r
    """

    b, g, r = cv2.split(src)
    cv2.addWeighted(b, 0.5, g, 0.5, 0, b)
    cv2.merge((b, b, r), dst)


def recolorRGV(src, dst):
    """ Simulate conversion from BGR to RGV (red, green, value).

        The source and destination images must both be in BGR format.
        Blues are desaturated.

        Pseudocode:
        dst.b = min(src.b, src.g, src.r)
        dst.g = src.g
        dst.r = src.r
    """

        b, g, r = cv2.split(src)
        cv2.min(b, g, b)
        cv2.min(b, r, b)
        cv2.merge((b, g, r), dst)


def recolorCMV(src, dst):
    """ Simulate conversion from BGR to CMV (cyan, magenta, value).

        The source and destination images must both be in BGR format.
        Yellows are desaturated.

        Pseudocode:
        dst.b = max(src.b, src.g, src.r)
        dst.g = src.g
        dst.r = src.r
    """

    b, g, r = cv2.split(src)
    cv2.max(b, g, b)
    cv2.max(b, r, b)
    cv2.merge((b, g, r), dst)


class VFuncFilter(object):
    """ A filter that applies a function to V (or all of BGR). """

    def __init__(self, vFunc=None, dtype=np.uint8):
        length = np.iinfo(dtype).max + 1
        self._vLookupArray = utils.createLookupArray(vFunc, length)


    def apply(self, src, dst):
        """ Apply the filter with a BGR or gray source/destination. """
        srcFlatView = utils.flatView(src)
        dstFlatView = utils.flatView(dst)
        utils.applyLookupArray(self._vLookupArray, srcFlatView, dstFlatView)


class VCurveFilter(VFuncFilter):
    """ A filter that applies a curve to V (or all of BGR). """

    def __init__(self, vPoints, dytpe=np.uint8):
        VFuncFilter.__init__(self, utils.createCurveFunc(vPoints), dytpe)


class BGRFuncFilter(object):
    """ A filter that applies different functions to each of BGR. """

    def __init__(self, vFunc=None, bFunc=None, gFunc=None, rFunc=None, dtype=np.uint8):
        length = np.iinfo(dtype).max + 1
        self._bLookupArray = utils.createLookupArray(utils.createCompositeFunc(bFunc, vFunc), length)
        self._gLookupArray = utils.createLookupArray(utils.createCompositeFunc(gFunc, vFunc), length)
        self._rLookupArray = utils.createLookupArray(utils.createCompositeFunc(rFunc, vFunc), length)


    def apply(self, src, dst):
        """ Apply the filter with a BGR source/destination. """
        b, g, r = cv2.split(src)
        utils.applyLookupArray(self._bLookupArray, b, b)
        utils.applyLookupArray(self._gLookupArray, g, g)
        utils.applyLookupArray(self._rLookupArray, r, r)
        cv2.merge([b, g, r], dst)


class BGRCurveFilter(BGRFuncFilter):
    """ A filter that applies different curves to each of BGR. """

    def __init__(self, vPoints=None, bPoints=None, gPoints=None, rPoints=None, dtype=np.uint8):
        BGRFuncFilter.__init__(self, utils.createCurveFunc(vPoints), utils.createCurveFunc(bPoints), utils.createCurveFunc(gPoints), utils.createCurveFunc(rPoints), dtype)















