import cv2
import mediapipe as mp
import numpy as np
import traceback
import os
import sys
import pathlib

path_arg = sys.argv[1]
dir = os.fsencode(rf'{path_arg}')


average_angles = {
     "right_wrist": [180,0],
     "left_wrist": [180,0],
     "right_elbow": [180,0],
     "left_elbow": [180,0],
     "right_shoulder": [180,0],
     "left_shoulder": [180,0],
     "right_hip": [180,0],
     "left_hip": [180,0],
     "right_knee": [180,0],
     "left_knee": [180,0],
     "right_ankle": [180,0],
     "left_ankle": [180,0],
}

def calculate_angle(start, mid, end):
        start = np.array(start)
        mid = np.array(mid)
        end = np.array(end)

        radians = np.arctan2(end[1]-mid[1], end[0]-mid[0]) - np.arctan2(start[1]-mid[1], start[0]-mid[0])
        angle = np.abs(radians*180/np.pi)
        if angle>180:
            angle = 360 - angle
        return angle

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

for filepath in pathlib.Path(rf'{path_arg}').glob('**/*'):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        print(filepath.absolute())
        cap = cv2.VideoCapture(os.fsdecode(filepath.absolute()))
        while True:
            ret, img = cap.read()

            if not np.any(img): break

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img.flags.writeable = False

            results = pose.process(img)

            img.flags.writeable = True
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            
            
            try:
                landmarks = results.pose_landmarks.landmark
                joints = {
                    "right_wrist": (
                        (landmarks[mp_pose.PoseLandmark.RIGHT_PINKY.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_PINKY.value].y),
                        (landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y),
                        (landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y)
                    ),
                    "left_wrist": (
                        (landmarks[mp_pose.PoseLandmark.LEFT_PINKY.value].x, landmarks[mp_pose.PoseLandmark.LEFT_PINKY.value].y),
                        (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y),
                        (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y)
                    ),
                    "right_elbow": (
                        (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y),
                        (landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y),
                        (landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y)
                    ),
                    "left_elbow": (
                        (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y),
                        (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y),
                        (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y)
                    ),
                    "right_shoulder": (
                        (landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y),
                        (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y),
                        (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y)
                    ),
                    "left_shoulder": (
                        (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y),
                        (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y),
                        (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y)
                    ),
                    "right_hip": (
                        (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y),
                        (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y),
                        (landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y)
                    ),
                    "left_hip": (
                        (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y),
                        (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y),
                        (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y)
                    ),
                    "right_knee": (
                        (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y),
                        (landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y),
                        (landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y)
                    ),
                    "left_knee": (
                        (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y),
                        (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y),
                        (landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y)
                    ),
                    "right_ankle": (
                        (landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y),
                        (landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y),
                        (landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y)
                    ),
                    "left_ankle": (
                        (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y),
                        (landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y),
                        (landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y)
                    )     
                }
                for joint in joints:
                    angle = calculate_angle(joints[joint][0],joints[joint][1],joints[joint][2])
                    if (angle>average_angles[joint][1]): average_angles[joint][1] = (average_angles[joint][1]+angle)/2
                    if (angle<average_angles[joint][0]): average_angles[joint][0] = (average_angles[joint][0]+angle)/2
            except:
                traceback.print_exc()



            mp_drawing.draw_landmarks(img,
                                    results.pose_landmarks,
                                    mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

            cv2.imshow("MediaPipe Feed", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
cap.release()


cv2.destroyAllWindows()

print(average_angles)

    