"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
from __future__ import division
import os
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
# webcam = cv2.VideoCapture(0)
video_root = '/home/himanshu/Downloads'
video_name = 'P45.avi'

if not os.path.exists(os.path.join(video_root, 'MIT_images', video_name[:-4])):
    os.mkdir(os.path.join(video_root, 'MIT_images', video_name[:-4]))
    os.system("ffmpeg -i {0}/{2} -vf fps=30 {0}/MIT_images/{1}/output%06d.png".format(video_root, video_name[:-4], video_name))
    # os.system("ffmpeg -i {0}/P45.avi -vf fps=30 {0}/MIT_images/{1}/output%06d.png".format(video_root, video_name[:-4]))

# while True:
    # We get a new frame from the webcam
img_root = '/home/himanshu/Downloads/MIT_images/P45'
left = 0
right = 0
center = 0
blinking = 0
for fname in os.listdir(img_root):
    frame = cv2.imread(os.path.join(img_root, fname))
    frame = gaze.perspective_transform(frame, angle_x=65, angle_y=50)
# print(frame.shape)
# We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
        blinking += 1
    elif gaze.is_right():
        text = "Looking right"
        right += 1
    elif gaze.is_left():
        text = "Looking left"
        left += 1
    elif gaze.is_center():
        text = "Looking center"
        center += 1

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
    # cv2.destroyAllWindows()
center_gaze_ratio = center/len(os.listdir(img_root))
right_gaze_ratio = right/len(os.listdir(img_root))
left_gaze_ratio = left/len(os.listdir(img_root))
blinking_ratio = blinking/len(os.listdir(img_root))
print("Gaze count: \n center:{0}, left: {1}, right: {2}, blink: {3}, total: {4}\n".format(center,
                                                                         left,
                                                                         right,
                                                                         blinking,
                                                                        len(os.listdir(img_root))))
print("Gaze Ratios: \n center:{0}, left: {1}, right: {2}, blink: {3}".format(center_gaze_ratio,
                                                                         left_gaze_ratio,
                                                                         right_gaze_ratio,
                                                                         blinking_ratio))