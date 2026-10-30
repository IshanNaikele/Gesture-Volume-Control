import cv2
import time
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import HandTrackingModule as htm

################################
wCam, hCam = 640, 480
CAMERA_INDEX = 0          # change to 1 if your webcam is not the default one
MIN_LEN, MAX_LEN = 50, 300  # thumb-index distance range (pixels)
SMOOTHNESS = 5            # volume % moves in steps of this value (0 = no smoothing)
################################

cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

# --- System volume setup (works with old and new pycaw versions) ---
speakers = AudioUtilities.GetSpeakers()
try:
    volume = speakers.EndpointVolume                      # newer pycaw
except AttributeError:
    interface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))  # older pycaw

volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    if not success:
        print("Could not read from camera. Try changing CAMERA_INDEX.")
        break

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # 4 = thumb tip, 8 = index finger tip
        length, img, lineInfo = detector.findDistance(4, 8, img)

        # Convert distance to volume
        vol = np.interp(length, [MIN_LEN, MAX_LEN], [minVol, maxVol])
        volBar = np.interp(length, [MIN_LEN, MAX_LEN], [400, 150])
        volPer = np.interp(length, [MIN_LEN, MAX_LEN], [0, 100])

        if SMOOTHNESS > 0:
            volPer = SMOOTHNESS * round(volPer / SMOOTHNESS)
            vol = np.interp(volPer, [0, 100], [minVol, maxVol])

        volume.SetMasterVolumeLevel(vol, None)

        # Fingers close together -> green dot
        if length < MIN_LEN:
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)

    # Volume bar
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if cTime != pTime else 0
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Gesture Volume Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):   # press q to quit
        break

cap.release()
cv2.destroyAllWindows()