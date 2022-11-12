import cv2


class MovementDetector():
    def __init__(self, cap):
        self.cap = cap
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

    def update(self):
        ret, self.frame = self.cap.read()
        height, width, _ = self.frame.shape
        

    def showMask(self):
        roi = self.frame[340: 720,500: 800]
        mask = self.object_detector.apply(roi)
        cv2.imshow("Mask", mask)

    def PercentageOfMovement(self, x1, x2, y1, y2):
        roi = self.frame[y1: y2,x1: x2]
        mask = self.object_detector.apply(roi)
        
        w = 0
        b = 0
        for i in mask:
            for j in i:
                if j:
                    w+=1
                    b+=1
                else:
                    b+=1
        return(100*(w/(b*100)))
        
