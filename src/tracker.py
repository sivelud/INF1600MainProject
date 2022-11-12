import cv2


class MovementDetector():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

    def update(self):
        ret, frame = self.cap.read()
        if frame is None:
            print("frame is none")
            return
        height, width, _ = frame.shape
        roi = frame[340: 720,500: 800]
        mask = self.object_detector.apply(roi)
        cv2.imshow("Mask", mask)

    def get_movement(self, x1, x2, y1, y2):
        ret, frame = self.cap.read()
        #height, width, _ = frame.shape
        roi = frame[y1: y2,x1: x2]
        mask = self.object_detector.apply(roi)
        cv2.imshow("Mask", mask)

        w = 0
        b = 0
        n = 0
        for i in mask:
            for j in i:
                if j:
                    w+= 1
                    b+= 1
                else:
                    b+= 1
        if w and b:
            n = 100*((w/(b*100))*100)

        print(int(n*100))

    
    def destroy(self):
        self.cap.release()
        cv2.destroyAllWindows()