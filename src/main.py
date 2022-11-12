from tracker import MovementDetector
import cv2

movement_detector = MovementDetector()

while True:
    
    movement_detector.update()

    key = cv2.waitKey(30)
    if key == 27:
        break

movement_detector.destroy()