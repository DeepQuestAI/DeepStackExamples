import numpy as np
import cv2
import requests

cap = cv2.VideoCapture(0)
out = cv2.VideoWriter("object_detection_from_camera_to_file.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
                                                ,24,((int(cap.get(3)), int(cap.get(4)))))

progress_tracker = 0
prediction_json = {}
skip_frame = 20
print('<============================= Press contrl + c to break ===============================>')

while(cap.isOpened()):
    valid, frame = cap.read()
    

    if valid == True:
        progress_tracker += 1

        if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/detection",
                                            files={"image":new_frame}).json()
            prediction_json = response['predictions']
            print(prediction_json)

        num_prediction_json = len(prediction_json)
        for i in range(num_prediction_json):

            color_space_values = np.random.randint(50, 255, size=(3,))
            red, green, blue = color_space_values
            red, green, blue = int(red), int(green), int(blue)
            
            frame = cv2.rectangle(frame, (prediction_json[i]['x_min'], prediction_json[i]['y_min']),
                                  (prediction_json[i]['x_max'], prediction_json[i]['y_max']), (red, green, blue), 1)
        out.write(frame)        
        
    else:
        break


cap.release()
out.release()
