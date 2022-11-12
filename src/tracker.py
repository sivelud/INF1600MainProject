import cv2


class MovementDetector():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

    def update(self):
        ret, frame = self.cap.read()
        height, width, _ = frame.shape
        roi = frame[340: 720,500: 800]
        mask = self.object_detector.apply(roi)
        cv2.imshow("Mask", mask)

    
    def destroy(self):
        self.cap.release()
        cv2.destroyAllWindows()