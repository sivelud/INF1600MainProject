import cv2

cap = cv2.VideoCapture(0)
        
object_detector = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=40)

#ret, frame = cap.read()

#height, width, _ = frame.shape

#roi = frame[0+100:height-100, 0+200:width-200]

roi = (50,200,50,200)

mask = object_detector.apply(roi)

_, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

cv2.imshow("Mask", mask)