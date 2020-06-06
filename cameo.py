import cv2
from managers import WindowManager, CaptureManager

class Cameo(object):
    """
    A class used to processes frames from a camera and keyboard events.
    """

    def __init__(self):
        self._windowManager = WindowManager('Cameo', self.onKeypress)
        self._captureManager = CaptureManager(cv2.VideoCapture(0), self._windowManager, True)