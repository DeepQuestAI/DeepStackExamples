import cv2
import numpy as np
import requests


cap = cv2.VideoCapture('furious.mp4')

progress_tracker = 0
response_label = ""
skip_frame = 20

while(cap.isOpened()):
    valid, frame = cap.read()
    
        
    if valid == True:
        progress_tracker += 1

        if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/scene",
                                                        files={"image":new_frame}).json()
            response_label = response['label']
            print(response_label)


        font = cv2.FONT_HERSHEY_PLAIN
        frame = cv2.putText(frame, '{}'.format(response_label), (25, 35), font, 3, (255, 255, 0), 1, cv2.LINE_AA)
        cv2.imshow('Image Viewer', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()