import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

# Variables for environment changes
wCam, hCam = 640, 480                                                           # Resolution of Camera (Width, Height)
frameR = 100                                                                    # Frame Reduction
smoothening = 7                                                                 # Smootheing Value


pTime = 0                                                                       # initiating Present Time = 0
plocX, plocY = 0, 0                                                             # initiating Previous Location X, Previous Location Y
clocX, clocY = 0, 0                                                             # initiating Current Location X, Current Location Y


# Checking is Camera is working
cap = cv2.VideoCapture(0)                                                       # parameter 0 for inbuilt camera
# Making Width and Height fixed of camera
cap.set(3, wCam)
cap.set(4, hCam)

# making object of HandDectector
detector = htm.handDetector(maxHands=1)                                         # maximum hand = 1
wScr, hScr = autopy.screen.size()                                               # get the Width and Height of Screen
# print(wScr, hScr)

while True:

    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)                                               # Finding Hand
    lmList, bbox = detector.findPosition(img)                                   # Finding the Positions of the Hand and creating bounding box
    # print(lmList)
    # print(bbox)

    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:                                                        # If lmList i.e Finger Anchor is not null

        # Getting Co-ordinates of Index and Middle Finger
        x1, y1 = lmList[8][1:]                                                  # limLIst [8]-> dontes Index Finger and we want first two elements (x1, y1)
        x2, y2 = lmList[12][1:]                                                 # limLIst [8]-> dontes Middle Finger and we want first two elements (x2, y2)
        # print(x1, y1, x2, y2)

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)           # bounding the area of movement the actualize the screen field

        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:

            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))              # Converting the x1 Value to width of Web camera and again coverting to width of Screen
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # print(x3, y3)

            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move Mouse
            autopy.mouse.move(wScr - clocX, clocY)                              # Fliping the Direction of mouse movement from camera direction (img is fliped)
            # print(wScr- clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)            # In moving mode big circle is shown on tip of Index  finger
            plocX, plocY = clocX, clocY

        # 8. Both Index and middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:

            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            # print(length)

            # 10. Click mouse if distance short
            if length < 30:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    # 11. Frame Rate
    cTime = time.time()                                                                                 # Current Time
    fps = 1 / (cTime - pTime)                                                                           # FPS = Current Time - Previous Time
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)                # cv2.putText( img, text, origin, fontface, fontscale, color, thickness)

    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)