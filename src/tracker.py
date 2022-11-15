import cv2
from playsound import playsound
import time
import random


class MovementDetector():
    def __init__(self, cap):
        self.cap = cap
        if not self.cap.isOpened():
            print("\nERROR:\n Camera failed to open. Reboot necessary. Remember to run cap.release() and cv2.destroyAllWindows() on exit.\n")

        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=40, varThreshold=80)
        ret, self.frame = self.cap.read()
        height, width, _ = self.frame.shape
        self.roi = self.frame[0: 1920,0: 1080]
        
        

    def update(self):
        ret, self.frame = self.cap.read()
        height, width, _ = self.frame.shape
        self.mask = self.object_detector.apply(self.roi)

    def showMask(self):
        cv2.namedWindow("Mask")
        cv2.moveWindow("Mask", 1000, 150)
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


    def PercentageOfMovement2(self, x1, x2, y1, y2):
        w = 0 # White pixels
        t = 0 # Total number of pixels
        n = 0

        dx = x2 - x1
        dy = y2 - y1

        # Goes over all pixels in mask
        for x in range(dx - 1):
            for y in range(dy - 1):
                if self.mask[y1 + y][x1 + x]:
                    w+=1
                    t+=1
                else:
                    t+=1
            
        # Percentage of pixels that are white
        if w and t:
            n = ((w/t))
        return(n)


    def updateRoi(self, x1, x2, y1, y2):
        self.roi = self.frame[y1: y2,x1: x2]

    def closeCamera(self):
        self.cap.release()
        


class Judge():
    def __init__(self, top_cutoff, sensitivity):
        self.top_cutoff = top_cutoff
        self.sensitivity = sensitivity
        self.greenLightBool = True
        self.tempBool = False
        self.time = time.time()
        self.timeLastLight = self.time + 1.5
        self.redLightTime = random.randint(1,5)
        self.greenLightTime = random.randint(2,7)

        playsound('sounds/introSquid.mp3', False)
        

    def update(self, movement):
        self.time = time.time()

        if not self.greenLightBool:
            if self.time - self.timeLastLight > 2.0:
                if movement > self.top_cutoff:
                    return False
                if movement > self.sensitivity:
                    return True

        self.autoChangeLight()
            

    def greenLight(self):
        self.greenLightBool = True
        playsound('sounds/greenLight.mp3', False)
        self.timeLastLight = self.time

    def redLight(self):
        playsound('sounds/redLight.mp3', False)
        self.greenLightBool = False
        self.timeLastLight = self.time

    def changeLight(self):
        print("Greenlight bool =",self.greenLightBool)
        self.greenLightBool = not self.greenLightBool
        if self.greenLightBool:
            self.greenLight()
        if not self.greenLightBool:
            self.redLight()

    def autoChangeLight(self):

        if self.greenLightBool:
            if self.time - self.timeLastLight > self.redLightTime:
                self.redLightTime = random.randint(1,5)
                self.changeLight()
                self.timeLastLight = self.time
                return

        if not self.greenLightBool:
            if self.time - self.timeLastLight > self.greenLightTime:
                self.greenLightTime = random.randint(3,7)
                self.changeLight()
                self.timeLastLight = self.time
                return
    
    