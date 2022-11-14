from tracker import MovementDetector
from tracker import Judge
from asone import asone
import cv2



# Movement Judge Parameters:
top_cutoff = 80 # Movement above this percentage will be ignored
sensitivity = 3 # Movement above this percentage will result in game over



movement_detector = MovementDetector()
judge = Judge(top_cutoff, sensitivity)
#judge.redLight()



while True:
    movement_detector.update()
    # Nessecary in order for the program to exit correctly. Will probably be obsolete later in the project.
    movement_detector.showMask()
    # Region of interest. The part of the screen that will be checked for movement
    movement_detector.updateRoi(0, 1920, 0, 1080)

    

    if judge.update(movement_detector.PercentageOfMovement()):
        print("GAME OVER!")
        break
    
    

    key = cv2.waitKey(30)
    if key == 27:
        break
    if key == 32:
        print("YOU WON!")
        judge.redLight()


# Always close camera on exit.
movement_detector.closeCamera()
cv2.destroyAllWindows()