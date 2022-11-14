from tracker import MovementDetector
from tracker import Judge
import argparse
import asone
from asone import ASOne
import cv2

def main(args):
    filter_classes = args.filter_classes

    if filter_classes:
        filter_classes = [filter_classes]

    dt_obj = ASOne(
        tracker=asone.BYTETRACK,
        detector=asone.YOLOX_DARKNET_PYTORCH,
        use_cuda=args.use_cuda
        )

    # Track using webcam
    track_fn = dt_obj.track_webcam(cam_id=0, output_dir='data/results', save_result=False, display=True)

    # Loop over track_fn to retrieve outputs of each frame 
    for bbox_details, frame_details in track_fn:
        bbox_xyxy, ids, scores, class_ids = bbox_details
        frame, frame_num, fps = frame_details

        if 0 in class_ids:
            # It's a human
            print("human")

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
