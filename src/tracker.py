import cv2


class MovementDetector():
    def __init__(self, cap):
        self.cap = cap
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
        ret, self.frame = self.cap.read()
        height, width, _ = self.frame.shape
        self.roi = self.frame[340: 720,500: 800]

    def update(self):
        ret, self.frame = self.cap.read()
        height, width, _ = self.frame.shape
        self.mask = self.object_detector.apply(self.roi)

    def showMask(self):
        cv2.imshow("Mask", self.mask)

    def PercentageOfMovement(self):
        w = 0 # White pixels
        t = 0 # Total number of pixels
        n = 0

        # Goes over all pixels in mask
        for i in self.mask:
            for j in i:
                if j:
                    w+=1
                    t+=1
                else:
                    t+=1
        # Percentage of pixels that are white
        if w and t:
            n = int(w/t*100)
        return(n)

    def updateRoi(self, x1, x2, y1, y2):
        self.roi = self.frame[y1: y2,x1: x2]