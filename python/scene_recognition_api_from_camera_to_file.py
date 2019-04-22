import cv2
import numpy as np
import requests


cap = cv2.VideoCapture(0)
out = cv2.VideoWriter("scene_recognition_from_camera_to_file.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                                    24,((int(cap.get(3)), int(cap.get(4)))))

progress_tracker = 0
response_label = ""
skip_frame = 20
print('<============================= Press contrl + c to break ===============================>')


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
        frame = cv2.putText(frame, '{}'.format(response_label), (25, 25), font, 1, (255, 255, 0), 1, cv2.LINE_AA)
        out.write(frame)        
        
    else:
        break

cap.release()
out.release()
