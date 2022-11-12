from tracker import MovementDetector
import cv2



cap = cv2.VideoCapture(0)

movement_detector = MovementDetector(cap)

running = False

if cap.isOpened():
    running = True
else:
    print("ERROR: Camera failed to open. This is probably because the program was not exited correctly")

while running:
    
    movement_detector.update()

    # Nessecary in order for the program to exit correctly. Will probably be obsolete later in the project.
    movement_detector.showMask()

    print(movement_detector.PercentageOfMovement())

    movement_detector.updateRoi(0, 1000, 0, 1000)

    key = cv2.waitKey(30)
    if key == 27:
        break

# Neccesary for the program to exit correctly. if not computer will need reboot for the camera to work again.
cap.release()
cv2.destroyAllWindows()