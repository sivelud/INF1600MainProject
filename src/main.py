from tracker import MovementDetector
import cv2



cap = cv2.VideoCapture(0)

movement_detector = MovementDetector(cap)

running = False

if cap.isOpened():
    running = True
else:
    print("ERROR: Camera failed to open")

while running:
    
    movement_detector.update()
    movement_detector.showMask()

    # Kills camera. needs fix
    print(movement_detector.PercentageOfMovement())

    key = cv2.waitKey(30)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()