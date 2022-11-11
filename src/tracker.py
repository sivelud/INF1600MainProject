import cv2

class MovementDetector():
    def __init__(self):
        # Bruker kamera feed
        self.cap = cv2.VideoCapture(0)
        # Lager en maske med MOG2
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=40)

        self.players = [PlayerTracker(100, 500, 100, 500), PlayerTracker(600, 900, 600, 900)]

    def update(self):
        for player in self.players:
            player.update(self.cap, self.object_detector)



class PlayerTracker():
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def update(self, cap, object_detector):
        self.ret, self.frame = self.cap.read()
        self.roi = self.frame[self.y1:self.y2, self.x1:self.x2]
        self.mask = self.object_detector.apply(self.roi)

        # 1. Object Detection
        self.mask = self.object_detector.apply(self.roi)

        _, self.mask = cv2.threshold(self.mask, 254, 255, cv2.THRESH_BINARY)

        self.n = 0
        for a in self.mask:
            for i in a:
                if i:
                    self.n += 1

    def printMovement(self):
        print(self.n)

    def showMask(self):
        cv2.imshow("Mask", self.mask)

    def resizeAreaOfInterest(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2