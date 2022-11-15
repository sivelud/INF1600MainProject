from tracker import MovementDetector
from tracker import Judge
import argparse
import AS_One.asone as asone
from AS_One.asone import ASOne
import cv2
from playsound import playsound
import os
import glob
import numpy as np

def main(args):
    # Remove elimenated players from previous game
    files = glob.glob('images/*')
    for f in files:
        os.remove(f)

    filter_classes = args.filter_classes

    if filter_classes:
        filter_classes = [filter_classes]

    dt_obj = ASOne(
        tracker=asone.BYTETRACK,
        detector=asone.YOLOX_DARKNET_PYTORCH,
        use_cuda=args.use_cuda
        )

    # Track using webcam
    cap = cv2.VideoCapture(0)

    track_fn = dt_obj.track_webcam(cap, output_dir='data/results', save_result=False, display=True)

    # Movement Judge Parameters:
    top_cutoff = 0.8 # Movement above this percentage will be ignored
    sensitivity = 0.02 # Movement above this percentage will result in game over

    movement_detector = MovementDetector(cap)
    judge = Judge(top_cutoff, sensitivity)

    game_over = False

    eliminated_players = []
    imgs = []

    # Loop over track_fn to retrieve outputs of each frame 
    for bbox_details, frame_details in track_fn:
        bbox_xyxy, ids, scores, class_ids = bbox_details
        frame, frame_num, fps = frame_details

        if game_over:
            break

        if 0 in class_ids:
            # It's a human

            movement_detector.update()
            # Nessecary in order for the program to exit correctly. Will probably be obsolete later in the project.
            movement_detector.showMask()
            # Region of interest. The part of the screen that will be checked for movement

            for i, box in enumerate(bbox_xyxy):
                x1, y1, x2, y2 = [int(i) for i in box]
                
                if x1 < 0:
                    x1 = 0
                if y1 < 0:
                    y1 = 0
                if x2 > 640:
                    x2 = 640
                if y2 > 480:
                    y2 = 480
                
                movement_detector.updateRoi(0, 1920, 0, 1080)

                movement_ratio = movement_detector.PercentageOfMovement2(x1, x2, y1, y2)   

                if judge.update(movement_ratio):
                    #game_over = True
                    print("GAME OVER!")

                    # Takes screenshot of elimanated player
                    if ids[i] not in eliminated_players and class_ids[i] == 0:
                        playsound('sounds/gunShot.mp3', False)
                        ret, img = cap.read()
                        crop_img = img[y1:y1+(y2-y1), x1:x1+(x2-x1)]
                        print("Player " + str(ids[i]) + "is eliminated!")
                        img_file = 'images/player_' + str(ids[i]) + '.png'
                        cv2.imwrite(img_file, crop_img)
                        eliminated_players.append(ids[i])

                        img_128 = cv2.resize(crop_img, (150, 200), interpolation = cv2.INTER_AREA)
                        imgs.append(img_128)
                        img_row = np.concatenate(imgs, axis=1)
                        cv2.namedWindow("Eliminated Players")
                        cv2.moveWindow("Eliminated Players", 800, 1000)
                        cv2.imshow('Eliminated Players', img_row)

                key = cv2.waitKey(30)
                if key == 27:
                    break
                if key == 32:
                    print("YOU WON!")
                    game_over = True
                    judge.redLight()


    # Always close camera on exit.
    movement_detector.closeCamera()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--video_path', help='Path to input video')
    parser.add_argument('--cpu', default=True, action='store_false', dest='use_cuda',
                        help='run on cpu if not provided the program will run on gpu.')
    parser.add_argument('--no_save', default=True, action='store_false',
                        dest='save_result', help='whether or not save results')
    parser.add_argument('--no_display', default=True, action='store_false',
                        dest='display', help='whether or not display results on screen')
    parser.add_argument('--output_dir', default='data/results',  help='Path to output directory')
    parser.add_argument('--draw_trails', default=False,  help='if provided object motion trails will be drawn.')
    parser.add_argument('--filter_classes', default=None, help='Filter class name')

    args = parser.parse_args()

    main(args)
