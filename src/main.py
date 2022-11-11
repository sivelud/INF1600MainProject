from tracker import *

"""
SOURCE: https://www.youtube.com/watch?v=O3b8lVF93jU
Copyed his sourcecode and modifyed it.
"""

tracker = MovementDetector()

while True:

    tracker.update()

    key = cv2.waitKey(30)
    if key == 27:
        break

tracker.cap.release()
cv2.destroyAllWindows()