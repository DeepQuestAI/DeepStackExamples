
# DeepStackExamples
## Example codes for DeepStack AI server
* [face_detection_api_from_camera_to_display.py](#1)
* [face_detection_api_from_camera_to_file.py](#2)
* [face_detection_api_from_video_to_display.py](#3)
* [face_detection_api_from_video_to_file.py](#4)
* [object_detection_api_from_camera_to_display.py](#5)
* [object_detection_api_from_camera_to_file.py](#6)
* [object_detection_api_from_video_to_display.py](#7)
* [object_detection_api_from_video_to_file.py](#8)
* [scene_recognition_api_from_camera_to_display.py](#9)
* [scene_recognition_api_from_camera_to_file.py](#10)
* [scene_recognition_api_from_video_to_display.py](#11)
* [scene_recognition_api_from_video_to_file.py](#12)

---

### face_detection_api_from_camera_to_display.py
<div id="1"></div>


```
import numpy as np
import cv2
import requests

cap = cv2.VideoCapture(0)

progress_tracker = 0
prediction_json = {}
skip_frame = 20
while(cap.isOpened()):
    valid, frame = cap.read()
    
        
    if valid == True:
        progress_tracker += 1

        if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/face",files={"image":new_frame}).json()
            prediction_json = response['predictions']
            print(prediction_json)

        num_prediction_json = len(prediction_json)
        for i in range(num_prediction_json):
            red, green, blue = 200, 100, 200
            frame = cv2.rectangle(frame, (prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']), (red, green, blue), 1)

        
        cv2.imshow('Image Viewer', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()
```
__Code break down__ 

```
import numpy as np
import cv2
import requests
```
> The three lines of code above is used to import **numpy** which is python numerical library on the first line, on the second line we imported opencv a computer vision library as **cv2**, and on line three we imported **request** which is a python library used for communicating with deepstack.

```
cap = cv2.VideoCapture(0)
```
> The code above is the **VideoCapture()** method is used by opencv to capture the video frame. While the argument **0** is just a number which specify which camera to be used.

```
progress_tracker = 0
prediction_json = {}
skip_frame = 20
```
> The three lines of code above is used to declare **progress_tracker** variable on the first line. On the second line we declare the **prediction_json** which is a dictionary which is stores the bounding box coordinates returned by Deepstack. On the third line we declare **skip_frame** variable which store the amount of frames to be skipped before face detection is performed by deepstack. If you want the face detection to be performed on every frame use the value of 1.

```
while(cap.isOpened()):
```
> In the line of code above we have **cap.isOpened()** which return the boolean value of 1 if the video capture as been initialized. The **while** loop will continue to run while the boolean value is 1.

```
valid, frame = cap.read()
```
>In the line of code above we have **cap.read()** which returns two values a bolean which can either 1 or 0 depend on if a video frame has been read or not, and the boolean values are stored in the **valid** variable. The second value returned by **cap.read()** is the video frame which is then stored in the **frame** variable.

```
if valid == True:
        progress_tracker += 1
```
>If **valid** on the first line has a boolean value of 1 the **if** code block below the will be executed. on the second line the **progress_tracker** variable will be incremented by 1.


```
if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/face",
                                                    files={"image":new_frame}).json()
            prediction_json = response['predictions']
            print(prediction_json)
```
>The first line of code `if(progress_tracker % skip_frame == 0)` checks if required number of video frames have been skipped then the code block in the **if** statement will be executed. On the second line we have `retval, new_frame = cv2.imencode('.jpg', frame)` and here the **cv2.imencode('.jpg', frame)** method compresses the video frame stored with **frame** argument into a memory buffer which is then passed to the **new_frame**. This method also takes in parameter like **.jpg** which is the extension that discribes the output format. On the third line we have `response = requests.post("http://localhost:80/v1/vision/face", files={"image":`**new_frame** `}).json()` that send a post request to the deepstack AI server, and the response a saved in the **response** variable. On the fourth line the respone predictions `response['predictions']` are store into the `prediction_json` variable. On the fifth line the predicted json that contains the bounding box coordinates returned by deepstack face_dectection API are been printed on the terminal with `print(prediction_json)`. 

```
num_prediction_json = len(prediction_json)
```
>This line of code gets the number of face whose bounding box coordinate are returned by deepstack AI server with `num_prediction_json = len(prediction_json)`.

```
for i in range(num_prediction_json):
            red, green, blue = 200, 100, 200
            frame = cv2.rectangle(frame, (prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']), (red, green, blue), 1)

```
>The first line of code `for i in range(num_prediction_json):` runs for the total number of predicted bounding box in `num_prediction_json` returned by deepstack. The second line of code `red, green, blue = 200, 100, 200` is the color values of the bounding boxes to be drawn. The third line of code is `cv2.rectangle()` method which is used for drawing the bounding boxes on the video frame. This method takes in five arguments which is the image `frame`, the top left coordinate and the bottom right coordinates for drawing the bounding box given by `(prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']),`, the color values `(red, green, blue)` the box thickness in pixel which is `1` in this case.

```
cv2.imshow('Image Viewer', frame)
```
>This method above display each video frame. It takes two argument the name of the view port window **'Image Viewer'** and the video frame **frame**.

```
if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```
>The if statement above only execute if the keyboard key **q** is press. When the key is press the code breaks out of the loop. The `cv.waitKey(1)` method listens for key press and `ord('q')` is an python method that returns an integer representing the Unicode code point of the character. The **0xFF** is used for case where the code is ran on a 64 bit machine.

```
 else:
        break
```
>The else code block only breaks the loop if the **valid** variable as a boolean value of 0.

```
cap.release()
cv2.destroyAllWindows()
```
>The `cap.release()` method closes video file or capturing device. while the `cv2.destroyAllWindows()` method destroys all the view port windows that were created.

---

### face_detection_api_from_camera_to_file.py
<div id="2"></div>

```
import numpy as np
import cv2
import requests

cap = cv2.VideoCapture(0)
out = cv2.VideoWriter("face_detection_from_camera_to_file.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),24,((int(cap.get(3)), int(cap.get(4)))))

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
            response = requests.post("http://localhost:80/v1/vision/face",files={"image":new_frame}).json()
            prediction_json = response['predictions']
            print(prediction_json)

        num_prediction_json = len(prediction_json)
        for i in range(num_prediction_json):
            red, green, blue = 100, 50, 200
            frame = cv2.rectangle(frame, (prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']), (red, green, blue), 1)
        out.write(frame)        
        
    else:
        break


cap.release()
out.release()
```
__Code break down__ 

```
import numpy as np
import cv2
import requests
```
> The three lines of code above is used to import **numpy** which is python numerical library on the first line, on the second line we imported opencv a computer vision library as **cv2**, and on line three we imported **request** which is a python library used for communicating with deepstack.

```
cap = cv2.VideoCapture(0)
```
> The code above is the **VideoCapture()** method is used by opencv to capture the video frames. While the argument **0** is just a number which specify which camera to be used.

```
out = cv2.VideoWriter("face_detection_from_camera_to_file.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24,((int(cap.get(3)), int(cap.get(4)))))

```
>The code above we have the `VideoWriter()` method which is used for writing videos. This method takes in four arguments which are the name the video will be save as `"face_detection_from_camera_to_file.avi"`, the codec for saving the video which is done with `cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')` method, the numbers of fames to save as per seconds; in this case we are saving at `24` frames per second. The last argument is the dimension for which the video is to be saved given by this `((int(cap.get(3)), int(cap.get(4)))))`, the `cap.get(3)` and `cap.get(4)` method returns the horizontal and vertical dimension of the capture video frames.

```
print('<============================= Press contrl + c to break ===============================>')
```
>This line of code print `'<============================= Press contrl + c to break ===============================>'` to the terminal telling the user what to do in other to terminate the code.

```
progress_tracker = 0
prediction_json = {}
skip_frame = 20
```
> The three lines of code above is used to declare **progress_tracker** variable on the first line. On the second line we declare the **pred_json** which is a dictionary which stores the bounding box coordinates returned by Deepstack. On the third line we declare **skip_frame** variable which store the amount of frames to be skipped before face detection is performed by deepstack. If you want the face detection to be performed on every frame use the value of 1.

```
while(cap.isOpened()):
```
> In the line of code above we have **cap.isOpened()** which return the boolean value of 1 if the video capture as been initialized. The **while** loop will continue to run while the boolean value is 1.

```
valid, frame = cap.read()
```
>In the line of code above we have **cap.read()** which returns two values a bolean which can either 1 or 0 depend on if a video frame has been read or not, and the boolean values are stored in the **valid** variable. The second value returned by **cap.read()** is the video frame which is then stored in the **frame** variable.

```
if valid == True:
        progress_tracker += 1
```
>If **valid** on the first line has a boolean value of 1 the **if** code block below the will be executed. on the second line the **progress_tracker** variable will be incremented by 1.


```
if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/face",
                                                    files={"image":new_frame}).json()
            prediction_json = response['predictions']
            print(prediction_json)
```
>The first line of code `if(progress_tracker % skip_frame == 0)` checks if required number of video frames have been skipped then the code block in the **if** statement will be executed. On the second line we have `retval, new_frame = cv2.imencode('.jpg', frame)` and here the **cv2.imencode('.jpg', frame)** method compresses the video frame stored with **frame** argument into a memory buffer which is then passed to the **new_frame**. This method also takes in parameter like **.jpg** which is athe extension that discribes the output format. On the third line we have `response = requests.post("http://localhost:80/v1/vision/face", files={"image":`**new_frame** `}).json()` that send a post request to the deepstack AI server, and the response a saved in the **response** variable. On the fourth line the respone predictions `response['predictions']` are store into the `prediction_json` variable. On the fifth line the predicted json that contains the bounding box coordinates returned by deepstack face_dectection API are been printed on the terminal with `print(prediction_json)`. 

```
num_prediction_json = len(prediction_json)
```
>This line of code gets the number of face whose bounding box coordinate are returned by deepstack AI server with `num_prediction_json = len(prediction_json)`.

```
for i in range(num_prediction_json):
            red, green, blue = 200, 100, 200
            frame = cv2.rectangle(frame, (prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']), (red, green, blue), 1)

```
>The first line of code `for i in range(num_prediction_json):` runs for the total number of predicted bounding box in `num_prediction_json` returned by deepstack. The second line of code `red, green, blue = 200, 100, 200` is the color values of the bounding boxes to be drawn. The third line of code is `cv2.rectangle()` method which is used for drawing the bounding boxes on the video frame. This method takes in five arguments which is the image `frame`, the top left coordinate and the bottom right coordinates for drawing the bounding box given by `(prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']),`, the color values `(red, green, blue)` the box thickness in pixel which is `1` in this case.


```
out.write(frame)  
```
>This method above is used to write each video frame. It takes one argument which is the video frame **frame**.

```
if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```
>The if statement above only execute if the keyboard key **"q"** is press. When the key is press the code breaks out of the loop. The `cv.waitKey(1)` method listens for key press and `ord('q')` is an python method that return an integer representing the Unicode code point of the character. the **0xFF** is used for case where the code is ran on a 64 bit machine.

```
 else:
        break
```
>The else code block only breaks the loop if the **valid** variable as a boolean value of 0.

```
cap.release()
out.release()
```
>The `cap.release()` and `out.release()` method closes video file or capturing device.

---
### face_detection_api_from_video_to_display.py
<div id="3"></div>


```
import numpy as np
import cv2
import requests


cap = cv2.VideoCapture('furious.mp4')

progress_tracker = 0
prediction_json = {} 
skip_frame = 20

while(cap.isOpened()):
    valid, frame = cap.read()
    
        
    if valid == True:
        progress_tracker += 1

        if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/face",files={"image":new_frame}).json()
            prediction_json = response['predictions']
            print(prediction_json)

        num_prediction_json = len(prediction_json)
        for i in range(num_prediction_json):
            red, green, blue = 100, 50, 200
            frame = cv2.rectangle(frame, (prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']), (red, green, blue), 1)

        
        cv2.imshow('Image Viewer', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()
```
__Code break down__ 

```
import numpy as np
import cv2
import requests
```
> The three lines of code above is used to import **numpy** which is python numerical library on the first line, on the secound line we imported opencv a computer vision library as **cv2**, and on line three we imported **request** which is a python library used for communicating with deepstack.

```
cap = cv2.VideoCapture('furious.mp4')
```
> The code above is the **VideoCapture()** method is used by opencv to read a video file, and it takes in the file to be read as argument. In this case it is **furious.mp4**.

```
progress_tracker = 0
prediction_json = {}
skip_frame = 20
```
> The three lines of code above is used to declare **progress_tracker** variable on the first line. On the second line we declare the **prediction_json** which is a dictionary which stores the bounding box coordinates returned by Deepstack. On the third line we declare **skip_frame** variable which store the amount of frames to be skipped before face detection is performed by deepstack. If you want the face detection to be performed on every frame use the value of 1.

```
while(cap.isOpened()):
```
> In the line of code above we have **cap.isOpened()** which return the boolean value of 1 if the video capture as been initialized. The **while** loop will continue to run while the boolean value is 1.

```
valid, frame = cap.read()
```
>In the line of code above we have **cap.read()** which returns two values a bolean which can either 1 or 0 depend on a video frame has been read or not, and the boolean values are stored in the **valid** variable. The second value returned by **cap.read()** is the video frame which is then stored in the **frame** variable.

```
if valid == True:
        progress_tracker += 1
```
>If **valid** on the first line has a boolean value of 1 the **if** code block below the will be executed. on the second line the **progress_tracker** variable will be incremented by 1.


```
if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/face",
                                                    files={"image":new_frame}).json()
            prediction_json = response['predictions']
            print(prediction_json)
```
>The first line of code `if(progress_tracker % skip_frame == 0)` checks if required number of video frames have been skipped then the code block in the **if** statement will be executed. On the second line we have `retval, new_frame = cv2.imencode('.jpg', frame)` and here the **cv2.imencode('.jpg', frame)** method compresses the video frame stored in **frame** argument into a memory buffer which is then passed to the **new_frame**. This method also takes in parameter like **.jpg** which is athe extension that discribes the output format. On the third line we have `response = requests.post("http://localhost:80/v1/vision/face", files={"image":`**new_frame** `}).json()` that send a post request to the deepstack AI server, and the response a saved in the **response** variable. On the fourth line the respone predictions `response['predictions']` are store into the `prediction_json` variable. On the fifth line the predicted json that contains the bounding box coordinates returned by deepstack face_dectection API are been printed on the terminal with `print(prediction_json)`. 

```
num_prediction_json = len(prediction_json)
```
>This line of code gets the number of face whose bounding box coordinate are returned by deepstack AI server with `num_prediction_json = len(prediction_json)`.

```
for i in range(num_prediction_json):
            red, green, blue = 200, 100, 200
            frame = cv2.rectangle(frame, (prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']), (red, green, blue), 1)

```
>The first line of code `for i in range(num_prediction_json):` runs for the total number of predicted bounding box in `num_prediction_json` returned by deepstack. The second line of code `red, green, blue = 200, 100, 200` is the color values of the bounding boxes to be drawn. The third line of code is `cv2.rectangle()` method which is used for drawing the bounding boxes on the video frame. This method takes in five arguments which is the image `frame`, the top left coordinate and the bottom right coordinates for drawing the bounding box given by `(prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']),`, the color values `(red, green, blue)` the box thickness in pixel which is `1` in this case.


```
cv2.imshow('Image Viewer', frame)
```
>This method above display each video frame. It takes two argument the name of the view port window **'Image Viewer'** and the video frame **frame**.

```
if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```
>The if statement above only execute if the keyboard key **q** is press. When the key is press the code breaks out of the loop. The `cv.waitKey(1)` method listens for key press and `ord('q')` is an python method that return an integer representing the Unicode code point of the character. the **0xFF** is used for case where the code is ran on a 64 bit machine.

```
 else:
        break
```
>The else code block only breaks the loop if the **valid** variable as a boolean value of 0.

```
cap.release()
cv2.destroyAllWindows()
```
>The `cap.release()` method closes video file or capturing device. while the `cv2.destroyAllWindows()` method destroys all the view port windows that were created.
---
### face_detection_api_from_video_to_file.py
<div id="4"></div>

```
import numpy as np
import cv2
import requests

cap = cv2.VideoCapture('furious.mp4')
out = cv2.VideoWriter("face_detection_from_video_to_file.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),24,((int(cap.get(3)), int(cap.get(4)))))

progress_tracker = 0
prediction_json = {}
skip_frame = 20

while(cap.isOpened()):
    valid, frame = cap.read()
    
        
    if valid == True:
        progress_tracker += 1

        if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/face",files={"image":new_frame}).json()
            prediction_json = response['predictions']
            print(prediction_json)

        num_prediction_json = len(prediction_json)
        for i in range(num_prediction_json):
            red, green, blue = 100, 50, 200
            frame = cv2.rectangle(frame, (prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']), (red, green, blue), 1)
        out.write(frame)        
        
    else:
        break

print('<==============Video file as been full written with face bounding boxes============>')

cap.release()
out.release()
```
__Code break down__ 

```
import numpy as np
import cv2
import requests
```
> The three lines of code above is used to import **numpy** which is python numerical library on the first line, on the second line we imported opencv a computer vision library as **cv2**, and on line three we imported **request** which is a python library used for communicating with deepstack.

```
cap = cv2.VideoCapture('furious.mp4')
```
> The code above is the **VideoCapture()** method is used by opencv to read a video file, and it takes in the file to be read as argument. In this case it is **furious.mp4**.

```
out = cv2.VideoWriter("face_detection_from_camera_to_file.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24,((int(cap.get(3)), int(cap.get(4)))))

```
>The code above we have the **VideoWriter()** method which is used for writing videos. This method takes in four arguments which are the name the video will be save as **"face_detection_from_camera_to_file.avi"**, the codec for saving the video which is done with `cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')` method, the numbers of fames to save as per seconds; in this case it is we are saving at 24 frames per second. The last argument is the dimension for which the video is to be saved given by this `((int(cap.get(3)), int(cap.get(4)))))`, the `cap.get(3)` and `cap.get(3)` method returns the horizontal and vertical dimension of the capture video frames.

```
progress_tracker = 0
prediction_json = {}
skip_frame = 20
```
> The three lines of code above is used to declare **progress_tracker** variable on the first line. On the second line we declare the **prediction_json** which is a dictionary whch is used the bounding box coordinates returned by Deepstack. On the third line we declare **skip_frame** variable which store the amount of frames to be skipped before face detection is performed by deepstack. If you want the face detection to be performed on every frame use the value of 1.

```
while(cap.isOpened()):
```
> In the line of code above we have **cap.isOpened()** which return the boolean value of 1 if the video capture as been initialized. The **while** loop will continue to run while the boolean value is 1.

```
valid, frame = cap.read()
```
>In the line of code above we have **cap.read()** which returns two values a bolean which can either 1 or 0 depend on a video frame has been read or not, and the boolean values are stored in the **valid** variable. The secound value returned by **cap.read()** is the video frame which is then stored in the **frame** variable.

```
if valid == True:
        progress_tracker += 1
```
>If **valid** on the first line has a boolean value of 1 the **if** code block below the will be executed. on the second line the **progress_tracker** variable will be incremented by 1.


```
if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/face",
                                                    files={"image":new_frame}).json()
            pred_json = response['predictions']
            print(pred_json)
```
>The first line of code `if(progress_tracker % skip_frame == 0)` checks if required number of video frames have been skipped then the code block in the **if** statement will be executed. On the second line we have `retval, new_frame = cv2.imencode('.jpg', frame)` and here the **cv2.imencode('.jpg', frame)** method compresses the video frame stored with **frame** argument into a memory buffer which is then passed to the **new_frame**. This method also takes in parameter like **.jpg** which is athe extension that discribes the output format. On the third line we have `response = requests.post("http://localhost:80/v1/vision/face", files={"image":`**new_frame** `}).json()` that send a post request to the deepstack AI server, and the response a saved in the **response** variable. On the fourth line the respone predictions `response['predictions']` are store into the `pred_json` variable. On the fifth line the predicted json that contains the bounding box coordinates returned by deepstack face_dectection API are been printed on the terminal with `print(pred_json)`. 

```
num_prediction_json = len(prediction_json)
```
>This line of code gets the number of face whose bounding box coordinate are returned by deepstack AI server with `num_prediction_json = len(prediction_json)`.

```
for i in range(num_prediction_json):
            red, green, blue = 200, 100, 200
            frame = cv2.rectangle(frame, (prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']), (red, green, blue), 1)

```
>The first line of code `for i in range(num_prediction_json):` runs for the total number of predicted bounding box in `num_prediction_json` returned by deepstack. The second line of code `red, green, blue = 200, 100, 200` is the color values of the bounding boxes to be drawn. The third line of code is `cv2.rectangle()` method which is used for drawing the bounding boxes on the video frame. This method takes in five arguments which is the image `frame`, the top left coordinate and the bottom right coordinates for drawing the bounding box given by `(prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']),`, the color values `(red, green, blue)` the box thickness in pixel which is `1` in this case.


```
out.write(frame)  
```
>This method above is used to write each video frame. It takes one argument which is the video frame **frame**.

```
if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```
>The if statement above only execute if the keyboard key **"q"** is press. When the key is press the code breaks out of the loop. The `cv.waitKey(1)` method listens for key press and `ord('q')` is an python method that return an integer representing the Unicode code point of the character. the **0xFF** is used for case where the code is ran on a 64 bit machine.

```
 else:
        break
```
>The else code block only breaks the loop if the **valid** variable as a boolean value of 0.
```
print('<==============Video file as been full written with face bounding boxes============>')
```
>This line of code print `'<==============Video file as been full written with face bounding boxes============>'` to the terminal telling the user that the video as been full written with face bounding boxes.

```
cap.release()
out.release()
```
>The `cap.release()` and `out.release()` method closes video file or capturing device.
---
### object_detection_api_from_camera_to_display.py
<div id="5"></div>

```
import numpy as np
import cv2
import requests

cap = cv2.VideoCapture(0)

progress_tracker = 0
prediction_json = {}
skip_frame = 20
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

        
        cv2.imshow('Image Viewer', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()

```
__Code break down__ 

```
import numpy as np
import cv2
import requests
```
> The three lines of code above is used to import **numpy** which is python numerical library on the first line, on the second line we imported opencv a computer vision library as **cv2**, and on line three we imported **request** which is a python library used for communicating with deepstack.

```
cap = cv2.VideoCapture(0)
```
> The code above is the **VideoCapture()** method is used by opencv to capture the video frame. While the argument **0** is just a number which specify which camera to be used.

```
progress_tracker = 0
prediction_json = {}
skip_frame = 20
```
> The three lines of code above is used to declare **progress_tracker** variable on the first line. On the second line we declare the **prediction_json** which is a dictionary which is stores the bounding box coordinates returned by Deepstack. On the third line we declare **skip_frame** variable which store the amount of frames to be skipped before object detection is performed by deepstack. If you want the object detection to be performed on every frame use the value of 1.

```
while(cap.isOpened()):
```
> In the line of code above we have **cap.isOpened()** which return the boolean value of 1 if the video capture as been initialized. The **while** loop will continue to run while the boolean value is 1.

```
valid, frame = cap.read()
```
>In the line of code above we have **cap.read()** which returns two values a bolean which can either 1 or 0 depend on if a video frame has been read or not, and the boolean values are stored in the **valid** variable. The second value returned by **cap.read()** is the video frame which is then stored in the **frame** variable.

```
if valid == True:
        progress_tracker += 1
```
>If **valid** on the first line has a boolean value of 1 the **if** code block below the will be executed. on the second line the **progress_tracker** variable will be incremented by 1.


```
if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/detection",
                                                    files={"image":new_frame}).json()
            prediction_json = response['predictions']
            print(prediction_json)
```
>The first line of code `if(progress_tracker % skip_frame == 0)` checks if required number of video frames have been skipped then the code block in the **if** statement will be executed. On the second line we have `retval, new_frame = cv2.imencode('.jpg', frame)` and here the **cv2.imencode('.jpg', frame)** method compresses the video frame stored with **frame** argument into a memory buffer which is then passed to the **new_frame**. This method also takes in parameter like **.jpg** which is the extension that discribes the output format. On the third line we have `response = requests.post("http://localhost:80/v1/vision/detection", files={"image":`**new_frame** `}).json()` that send a post request to the deepstack AI server, and the response a saved in the **response** variable. On the fourth line the respone predictions `response['predictions']` are store into the `prediction_json` variable. On the fifth line the predicted json that contains the bounding box coordinates returned by deepstack object_dectection API are been printed on the terminal with `print(prediction_json)`. 

```
num_prediction_json = len(prediction_json)
```
>This line of code gets the number of objects whose bounding box coordinate are returned by deepstack AI server with `num_prediction_json = len(prediction_json)`.

```
for i in range(num_prediction_json):

            color_space_values = np.random.randint(50, 255, size=(3,))
            red, green, blue = color_space_values
            red, green, blue = int(red), int(green), int(blue)
            
            frame = cv2.rectangle(frame, (prediction_json[i]['x_min'], prediction_json[i]['y_min']),
                       (prediction_json[i]['x_max'], prediction_json[i]['y_max']), (red, green, blue), 1)

```
>The first line of code `for i in range(num_prediction_json):` runs for the total number of predicted bounding box in `num_prediction_json` returned by deepstack.The second line of code `color_space_values = np.random.randint(50, 255, size=(3,))`is used to generate random color values between 50 and 255. The value represent the RGB color for the bounding box. In the third line of code the RGB value are extraced `red, green, blue = color_space_values`. In the fourth line of code the RGB values are converted to integer type `red, green, blue = int(red), int(green), int(blue)`. The fifth line of code is the  `cv2.rectangle()` method which is used for drawing the bounding boxes on the video frame. This method takes in five arguments which is the image `frame`, the top left coordinate and the bottom right coordinates for drawing the bounding box given by `(prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']),`, the color values `(red, green, blue)` the box thickness in pixel which is `1` in this case.


```
cv2.imshow('Image Viewer', frame)
```
>This method above display each video frame. It takes two argument the name of the view port window **'Image Viewer'** and the video frame **frame**.

```
if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```
>The if statement above only execute if the keyboard key **q** is press. When the key is press the code breaks out of the loop. The `cv.waitKey(1)` method listens for key press and `ord('q')` is an python method that returns an integer representing the Unicode code point of the character. The **0xFF** is used for case where the code is ran on a 64 bit machine.

```
 else:
        break
```
>The else code block only breaks the loop if the **valid** variable as a boolean value of 0.

```
cap.release()
cv2.destroyAllWindows()
```
>The `cap.release()` method closes video file or capturing device. while the `cv2.destroyAllWindows()` method destroys all the view port windows that were created.
---

### object_detection_api_from_camera_to_file.py
<div id="6"></div>

```
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

```
__Code break down__ 

```
import numpy as np
import cv2
import requests
```
> The three lines of code above is used to import **numpy** which is python numerical library on the first line, on the second line we imported opencv a computer vision library as **cv2**, and on line three we imported **request** which is a python library used for communicating with deepstack.

```
cap = cv2.VideoCapture(0)
```
> The code above is the **VideoCapture()** method is used by opencv to capture the video frames. While the argument **0** is just a number which specify which camera to be used.

```
out = cv2.VideoWriter("face_detection_from_camera_to_file.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24,((int(cap.get(3)), int(cap.get(4)))))

```
>The code above we have the `VideoWriter()` method which is used for writing videos. This method takes in four arguments which are the name the video will be save as `"face_detection_from_camera_to_file.avi"`, the codec for saving the video which is done with `cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')` method, the numbers of fames to save as per seconds; in this case we are saving at `24` frames per second. The last argument is the dimension for which the video is to be saved given by this `((int(cap.get(3)), int(cap.get(4)))))`, the `cap.get(3)` and `cap.get(4)` method returns the horizontal and vertical dimension of the capture video frames.

```
print('<============================= Press contrl + c to break ===============================>')
```
>This line of code print `'<============================= Press contrl + c to break ===============================>'` to the terminal telling the user what to do in other to terminate the code.

```
progress_tracker = 0
prediction_json = {}
skip_frame = 20
```
> The three lines of code above is used to declare **progress_tracker** variable on the first line. On the second line we declare the **pred_json** which is a dictionary which stores the bounding box coordinates returned by Deepstack. On the third line we declare **skip_frame** variable which store the amount of frames to be skipped before object detection is performed by deepstack. If you want the object detection to be performed on every frame use the value of 1.

```
while(cap.isOpened()):
```
> In the line of code above we have **cap.isOpened()** which return the boolean value of 1 if the video capture as been initialized. The **while** loop will continue to run while the boolean value is 1.

```
valid, frame = cap.read()
```
>In the line of code above we have **cap.read()** which returns two values a bolean which can either 1 or 0 depend on if a video frame has been read or not, and the boolean values are stored in the **valid** variable. The second value returned by **cap.read()** is the video frame which is then stored in the **frame** variable.

```
if valid == True:
        progress_tracker += 1
```
>If **valid** on the first line has a boolean value of 1 the **if** code block below the will be executed. on the second line the **progress_tracker** variable will be incremented by 1.


```
if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/detection",
                                                    files={"image":new_frame}).json()
            prediction_json = response['predictions']
            print(prediction_json)
```
>The first line of code `if(progress_tracker % skip_frame == 0)` checks if required number of video frames have been skipped then the code block in the **if** statement will be executed. On the second line we have `retval, new_frame = cv2.imencode('.jpg', frame)` and here the **cv2.imencode('.jpg', frame)** method compresses the video frame stored with **frame** argument into a memory buffer which is then passed to the **new_frame**. This method also takes in parameter like **.jpg** which is athe extension that discribes the output format. On the third line we have `response = requests.post("http://localhost:80/v1/vision/detection", files={"image":`**new_frame** `}).json()` that send a post request to the deepstack AI server, and the response a saved in the **response** variable. On the fourth line the respone predictions `response['predictions']` are store into the `prediction_json` variable. On the fifth line the predicted json that contains the bounding box coordinates returned by deepstack object_dectection API are been printed on the terminal with `print(prediction_json)`. 

```
num_prediction_json = len(prediction_json)
```
>This line of code gets the number of objects whose bounding box coordinate are returned by deepstack AI server with `num_prediction_json = len(prediction_json)`.


```
for i in range(num_prediction_json):

            color_space_values = np.random.randint(50, 255, size=(3,))
            red, green, blue = color_space_values
            red, green, blue = int(red), int(green), int(blue)
            
            frame = cv2.rectangle(frame, (prediction_json[i]['x_min'], prediction_json[i]['y_min']),
                       (prediction_json[i]['x_max'], prediction_json[i]['y_max']), (red, green, blue), 1)

```
>The first line of code `for i in range(num_prediction_json):` runs for the total number of predicted bounding box in `num_prediction_json` returned by deepstack.The second line of code `color_space_values = np.random.randint(50, 255, size=(3,))`is used to generate random color values between 50 and 255. The value represent the RGB color for the bounding box. In the third line of code the RGB value are extraced `red, green, blue = color_space_values`. In the fourth line of code the RGB values are converted to integer type `red, green, blue = int(red), int(green), int(blue)`. The fifth line of code is the  `cv2.rectangle()` method which is used for drawing the bounding boxes on the video frame. This method takes in five arguments which is the image `frame`, the top left coordinate and the bottom right coordinates for drawing the bounding box given by `(prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']),`, the color values `(red, green, blue)` the box thickness in pixel which is `1` in this case.


```
out.write(frame)  
```
>This method above is used to write each video frame. It takes one argument which is the video frame **frame**.

```
if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```
>The if statement above only execute if the keyboard key **"q"** is press. When the key is press the code breaks out of the loop. The `cv.waitKey(1)` method listens for key press and `ord('q')` is an python method that return an integer representing the Unicode code point of the character. the **0xFF** is used for case where the code is ran on a 64 bit machine.

```
 else:
        break
```
>The else code block only breaks the loop if the **valid** variable as a boolean value of 0.

```
cap.release()
out.release()
```
>The `cap.release()` and `out.release()` method closes video file or capturing device.
---

### object_detection_api_from_video_to_display.py
<div id="7"></div>

```
import numpy as np
import cv2
import requests

cap = cv2.VideoCapture('furious.mp4')

progress_tracker = 0
prediction_json = {}
skip_frame = 20

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

        
        cv2.imshow('Image Viewer', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()
```

__Code break down__ 

```
import numpy as np
import cv2
import requests
```
> The three lines of code above is used to import **numpy** which is python numerical library on the first line, on the secound line we imported opencv a computer vision library as **cv2**, and on line three we imported **request** which is a python library used for communicating with deepstack.

```
cap = cv2.VideoCapture('furious.mp4')
```
> The code above is the **VideoCapture()** method is used by opencv to read a video file, and it takes in the file to be read as argument. In this case it is **furious.mp4**.

```
progress_tracker = 0
prediction_json = {}
skip_frame = 20
```
> The three lines of code above is used to declare **progress_tracker** variable on the first line. On the second line we declare the **prediction_json** which is a dictionary which stores the bounding box coordinates returned by Deepstack. On the third line we declare **skip_frame** variable which store the amount of frames to be skipped before object detection is performed by deepstack. If you want the object detection to be performed on every frame use the value of 1.

```
while(cap.isOpened()):
```
> In the line of code above we have **cap.isOpened()** which return the boolean value of 1 if the video capture as been initialized. The **while** loop will continue to run while the boolean value is 1.

```
valid, frame = cap.read()
```
>In the line of code above we have **cap.read()** which returns two values a bolean which can either 1 or 0 depend on a video frame has been read or not, and the boolean values are stored in the **valid** variable. The second value returned by **cap.read()** is the video frame which is then stored in the **frame** variable.

```
if valid == True:
        progress_tracker += 1
```
>If **valid** on the first line has a boolean value of 1 the **if** code block below the will be executed. on the second line the **progress_tracker** variable will be incremented by 1.


```
if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/face",
                                                    files={"image":new_frame}).json()
            prediction_json = response['predictions']
            print(prediction_json)
```
>The first line of code `if(progress_tracker % skip_frame == 0)` checks if required number of video frames have been skipped then the code block in the **if** statement will be executed. On the second line we have `retval, new_frame = cv2.imencode('.jpg', frame)` and here the **cv2.imencode('.jpg', frame)** method compresses the video frame stored in **frame** argument into a memory buffer which is then passed to the **new_frame**. This method also takes in parameter like **.jpg** which is athe extension that discribes the output format. On the third line we have `response = requests.post("http://localhost:80/v1/vision/face", files={"image":`**new_frame** `}).json()` that send a post request to the deepstack AI server, and the response a saved in the **response** variable. On the fourth line the respone predictions `response['predictions']` are store into the `prediction_json` variable. On the fifth line the predicted json that contains the bounding box coordinates returned by deepstsck face_dectection API are been printed on the terminal with `print(prediction_json)`. 

```
num_prediction_json = len(prediction_json)
```
>This line of code gets the number of face whose bounding box coordinate are returned by deepstack AI server with `num_prediction_json = len(prediction_json)`.


```
for i in range(num_prediction_json):

            color_space_values = np.random.randint(50, 255, size=(3,))
            red, green, blue = color_space_values
            red, green, blue = int(red), int(green), int(blue)
            
            frame = cv2.rectangle(frame, (prediction_json[i]['x_min'], prediction_json[i]['y_min']),
                       (prediction_json[i]['x_max'], prediction_json[i]['y_max']), (red, green, blue), 1)

```
>The first line of code `for i in range(num_prediction_json):` runs for the total number of predicted bounding box in `num_prediction_json` returned by deepstack.The second line of code `color_space_values = np.random.randint(50, 255, size=(3,))`is used to generate random color values between 50 and 255. The value represent the RGB color for the bounding box. In the third line of code the RGB value are extraced `red, green, blue = color_space_values`. In the fourth line of code the RGB values are converted to integer type `red, green, blue = int(red), int(green), int(blue)`. The fifth line of code is the  `cv2.rectangle()` method which is used for drawing the bounding boxes on the video frame. This method takes in five arguments which is the image `frame`, the top left coordinate and the bottom right coordinates for drawing the bounding box given by `(prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']),`, the color values `(red, green, blue)` the box thickness in pixel which is `1` in this case.


```
cv2.imshow('Image Viewer', frame)
```
>This method above display each video frame. It takes two argument the name of the view port window**'Image Viewer'** and the video frame **frame**.

```
if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```
>The if statement above only execute if the keyboard key **q** is press. When the key is press the code breaks out of the loop. The `cv.waitKey(1)` method listens for key press and `ord('q')` is an python method that return an integer representing the Unicode code point of the character. the **0xFF** is used for case where the code is ran on a 64 bit machine.

```
 else:
        break
```
>The else code block only breaks the loop if the **valid** variable as a boolean value of 0.

```
cap.release()
cv2.destroyAllWindows()
```
>The `cap.release()` method closes video file or capturing device. while the `cv2.destroyAllWindows()` method destroys all the view port windows that were created.

---
### object_detection_api_from_video_to_file.py
<div id="8"></div>

```
import numpy as np
import cv2
import requests

cap = cv2.VideoCapture('furious.mp4')
out = cv2.VideoWriter("object_detection_from_video_to_file.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                                    24,((int(cap.get(3)), int(cap.get(4)))))

progress_tracker = 0
prediction_json = {}
skip_frame = 20

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

print('<==============Video file as been full written with object detection bounding boxes============>')

cap.release()
out.release()
```

__Code break down__ 

```
import numpy as np
import cv2
import requests
```
> The three lines of code above is used to import **numpy** which is python numerical library on the first line, on the second line we imported opencv a computer vision library as **cv2**, and on line three we imported **request** which is a python library used for communicating with deepstack.

```
cap = cv2.VideoCapture('furious.mp4')
```
> The code above is the **VideoCapture()** method is used by opencv to read a video file, and it takes in the file to be read as argument. In this case it is **furious.mp4**.

```
out = cv2.VideoWriter("face_detection_from_camera_to_file.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24,((int(cap.get(3)), int(cap.get(4)))))

```
>The code above we have the **VideoWriter()** method which is used for writing videos. This method takes in four arguments which are the name the video will be save as **"face_detection_from_camera_to_file.avi"**, the codec for saving the video which is done with `cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')` method, the numbers of fames to save as per seconds; in this case it is we are saving at 24 frames per second. The last argument is the dimension for which the video is to be saved given by this `((int(cap.get(3)), int(cap.get(4)))))`, the `cap.get(3)` and `cap.get(3)` method returns the horizontal and vertical dimension of the capture video frames.

```
progress_tracker = 0
prediction_json = {}
skip_frame = 20
```
> The three lines of code above is used to declare **progress_tracker** variable on the first line. On the second line we declare the **prediction_json** which is a dictionary whch is used the bounding box coordinates returned by Deepstack. On the third line we declare **skip_frame** variable which store the amount of frames to be skipped before object detection is performed by deepstack. If you want the object detection to be performed on every frame use the value of 1.

```
while(cap.isOpened()):
```
> In the line of code above we have **cap.isOpened()** which return the boolean value of 1 if the video capture as been initialized. The **while** loop will continue to run while the boolean value is 1.

```
valid, frame = cap.read()
```
>In the line of code above we have **cap.read()** which returns two values a bolean which can either 1 or 0 depend on a video frame has been read or not, and the boolean values are stored in the **valid** variable. The secound value returned by **cap.read()** is the video frame which is then stored in the **frame** variable.

```
if valid == True:
        progress_tracker += 1
```
>If **valid** on the first line has a boolean value of 1 the **if** code block below the will be executed. on the second line the **progress_tracker** variable will be incremented by 1.


```
if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/face",
                                                    files={"image":new_frame}).json()
            pred_json = response['predictions']
            print(pred_json)
```
>The first line of code `if(progress_tracker % skip_frame == 0)` checks if required number of video frames have been skipped then the code block in the **if** statement will be executed. On the second line we have `retval, new_frame = cv2.imencode('.jpg', frame)` and here the **cv2.imencode('.jpg', frame)** method compresses the video frame stored with **frame** argument into a memory buffer which is then passed to the **new_frame**. This method also takes in parameter like **.jpg** which is athe extension that discribes the output format. On the third line we have `response = requests.post("http://localhost:80/v1/vision/face", files={"image":`**new_frame** `}).json()` that send a post request to the deepstack AI server, and the response a saved in the **response** variable. On the fourth line the respone predictions `response['predictions']` are store into the `pred_json` variable. On the fifth line the predicted json that contains the bounding box coordinates returned by deepstsck face_dectection API are been printed on the terminal with `print(pred_json)`. 

```
num_prediction_json = len(prediction_json)
```
>This line of code gets the number of objects whose bounding box coordinate are returned by deepstack AI server with `num_prediction_json = len(prediction_json)`.


```
for i in range(num_prediction_json):

            color_space_values = np.random.randint(50, 255, size=(3,))
            red, green, blue = color_space_values
            red, green, blue = int(red), int(green), int(blue)
            
            frame = cv2.rectangle(frame, (prediction_json[i]['x_min'], prediction_json[i]['y_min']),
                       (prediction_json[i]['x_max'], prediction_json[i]['y_max']), (red, green, blue), 1)

```
>The first line of code `for i in range(num_prediction_json):` runs for the total number of predicted bounding box in `num_prediction_json` returned by deepstack.The second line of code `color_space_values = np.random.randint(50, 255, size=(3,))`is used to generate random color values between 50 and 255. The value represent the RGB color for the bounding box. In the third line of code the RGB value are extraced `red, green, blue = color_space_values`. In the fourth line of code the RGB values are converted to integer type `red, green, blue = int(red), int(green), int(blue)`. The fifth line of code is the  `cv2.rectangle()` method which is used for drawing the bounding boxes on the video frame. This method takes in five arguments which is the image `frame`, the top left coordinate and the bottom right coordinates for drawing the bounding box given by `(prediction_json[i]['x_min'], prediction_json[i]['y_min']),(prediction_json[i]['x_max'], prediction_json[i]['y_max']),`, the color values `(red, green, blue)` the box thickness in pixel which is `1` in this case.


```
out.write(frame)  
```
>This method above is used to write each video frame. It takes one argument which is the video frame **frame**.

```
if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```
>The if statement above only execute if the keyboard key **"q"** is press. When the key is press the code breaks out of the loop. The `cv.waitKey(1)` method listens for key press and `ord('q')` is an python method that return an integer representing the Unicode code point of the character. the **0xFF** is used for case where the code is ran on a 64 bit machine.

```
 else:
        break
```
>The else code block only breaks the loop if the **valid** variable as a boolean value of 0.
```
print('<=============Video file as been full written with object detection bounding boxes============>')
```
>This line of code print `'<==============Video file as been full written with object detection bounding boxes============>'` to the terminal telling the user that the video as been full written with object detection bounding boxes.

```
cap.release()
out.release()
```
>The `cap.release()` and `out.release()` method closes video file or capturing device.
---

### scene_recognition_api_from_camera_to_display.py
<div id="9"></div>

```
import cv2
import numpy as np
import requests


cap = cv2.VideoCapture(0)

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
```
__Code break down__ 

```
import numpy as np
import cv2
import requests
```
> The three lines of code above is used to import **numpy** which is python numerical library on the first line, on the second line we imported opencv a computer vision library as **cv2**, and on line three we imported **request** which is a python library used for communicating with deepstack.

```
cap = cv2.VideoCapture(0)
```
> The code above is the **VideoCapture()** method is used by opencv to capture the video frame. While the argument **0** is just a number which specify which camera to be used.

```
progress_tracker = 0
response_label = ""
skip_frame = 20
```
> The three lines of code above is used to declare **progress_tracker** variable on the first line. On the second line we declare the **response_label** which is stores the scene label returned by Deepstack. On the third line we declare **skip_frame** variable which store the amount of frames to be skipped before scene detection is performed by deepstack. If you want the scene detection to be performed on every frame use the value of 1.

```
while(cap.isOpened()):
```
> In the line of code above we have **cap.isOpened()** which return the boolean value of 1 if the video capture as been initialized. The **while** loop will continue to run while the boolean value is 1.

```
valid, frame = cap.read()
```
>In the line of code above we have **cap.read()** which returns two values a bolean which can either 1 or 0 depend on if a video frame has been read or not, and the boolean values are stored in the **valid** variable. The second value returned by **cap.read()** is the video frame which is then stored in the **frame** variable.

```
if valid == True:
        progress_tracker += 1
```
>If **valid** on the first line has a boolean value of 1 the **if** code block below the will be executed. on the second line the **progress_tracker** variable will be incremented by 1.


```
if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/scene",
                                                        files={"image":new_frame}).json()
            response_label = response['label']
            print(response_label)
```
>The first line of code `if(progress_tracker % skip_frame == 0)` checks if required number of video frames have been skipped then the code block in the **if** statement will be executed. On the second line we have `retval, new_frame = cv2.imencode('.jpg', frame)` and here the **cv2.imencode('.jpg', frame)** method compresses the video frame stored with **frame** argument into a memory buffer which is then passed to the **new_frame**. This method also takes in parameter like **.jpg** which is the extension that discribes the output format. On the third line we have `response = requests.post("http://localhost:80/v1/vision/detection", files={"image":`**new_frame** `}).json()` that send a post request to the deepstack AI server, and the response a saved in the **response** variable. On the fourth line the `response['label']` are store into the `response_label` variable. On the fifth line the response label that contains the label returned by deepstack object_dectection API are been printed on the terminal with `print('response_label')`. 

```
font = cv2.FONT_HERSHEY_PLAIN
frame = cv2.putText(frame, '{}'.format(resp_label), (25, 35), font, 3, (255, 255, 0), 1, cv2.LINE_AA)
```
>The first line of code set the font type which the text will be written with using this constant `cv2.FONT_HERSHEY_PLAIN`. While on the second line the `cv2.putText()` method is used to write text on the video frame, and takes in nine arguments which includes the video frame `frame` the text to be displayed which in this case is the response label give by `'{}'.format(resp_label)`, the distace from the top left position where the text will be displayed which is given by `(25, 35)`, the font which is `font`, the text size in points which is `3` in this case, the color space value in RGB give by `(255, 255, 0)` how bold the text should be in points which is `1` in this case, and the kind of line which in this case is `cv2.LINE_AA` which is anti-aliased line which looks great for curves.

```
cv2.imshow('Image Viewer', frame)
```
>This method above display each video frame. It takes two argument the name of the view port window **'Image Viewer'** and the video frame **frame**.

```
if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```
>The if statement above only execute if the keyboard key **q** is press. When the key is press the code breaks out of the loop. The `cv.waitKey(1)` method listens for key press and `ord('q')` is an python method that returns an integer representing the Unicode code point of the character. The **0xFF** is used for case where the code is ran on a 64 bit machine.

```
 else:
        break
```
>The else code block only breaks the loop if the **valid** variable as a boolean value of 0.

```
cap.release()
cv2.destroyAllWindows()
```
>The `cap.release()` method closes video file or capturing device. while the `cv2.destroyAllWindows()` method destroys all the view port windows that were created.
---

### scene_recognition_api_from_camera_to_file.py
<div id="10"></div>

```
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

```
__Code break down__ 

```
import numpy as np
import cv2
import requests
```
> The three lines of code above is used to import **numpy** which is python numerical library on the first line, on the second line we imported opencv a computer vision library as **cv2**, and on line three we imported **request** which is a python library used for communicating with deepstack.

```
cap = cv2.VideoCapture(0)
```
> The code above is the **VideoCapture()** method is used by opencv to capture the video frames. While the argument **0** is just a number which specify which camera to be used.

```
out = cv2.VideoWriter("face_detection_from_camera_to_file.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24,((int(cap.get(3)), int(cap.get(4)))))

```
>The code above we have the `VideoWriter()` method which is used for writing videos. This method takes in four arguments which are the name the video will be save as `"face_detection_from_camera_to_file.avi"`, the codec for saving the video which is done with `cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')` method, the numbers of fames to save as per seconds; in this case we are saving at `24` frames per second. The last argument is the dimension for which the video is to be saved given by this `((int(cap.get(3)), int(cap.get(4)))))`, the `cap.get(3)` and `cap.get(4)` method returns the horizontal and vertical dimension of the capture video frames.

```
print('<============================= Press contrl + c to break ===============================>')
```
>This line of code print `'<============================= Press contrl + c to break ===============================>'` to the terminal telling the user what to do in other to terminate the code.

```
progress_tracker = 0
response_label = ""
skip_frame = 20
```
> The three lines of code above is used to declare **progress_tracker** variable on the first line. On the second line we declare the **response_label** which is stores the scene label returned by Deepstack. On the third line we declare **skip_frame** variable which store the amount of frames to be skipped before scene detection is performed by deepstack. If you want the scene detection to be performed on every frame use the value of 1.

```
while(cap.isOpened()):
```
> In the line of code above we have **cap.isOpened()** which return the boolean value of 1 if the video capture as been initialized. The **while** loop will continue to run while the boolean value is 1.

```
valid, frame = cap.read()
```
>In the line of code above we have **cap.read()** which returns two values a bolean which can either 1 or 0 depend on if a video frame has been read or not, and the boolean values are stored in the **valid** variable. The second value returned by **cap.read()** is the video frame which is then stored in the **frame** variable.

```
if valid == True:
        progress_tracker += 1
```
>If **valid** on the first line has a boolean value of 1 the **if** code block below the will be executed. on the second line the **progress_tracker** variable will be incremented by 1.


```
if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/scene",
                                                        files={"image":new_frame}).json()
            response_label = response['label']
            print(response_label)
```
>The first line of code `if(progress_tracker % skip_frame == 0)` checks if required number of video frames have been skipped then the code block in the **if** statement will be executed. On the second line we have `retval, new_frame = cv2.imencode('.jpg', frame)` and here the **cv2.imencode('.jpg', frame)** method compresses the video frame stored with **frame** argument into a memory buffer which is then passed to the **new_frame**. This method also takes in parameter like **.jpg** which is the extension that discribes the output format. On the third line we have `response = requests.post("http://localhost:80/v1/vision/detection", files={"image":`**new_frame** `}).json()` that send a post request to the deepstack AI server, and the response a saved in the **response** variable. On the fourth line the `response['label']` are store into the `response_label` variable. On the fifth line the response label that contains the label returned by deepstack object_dectection API are been printed on the terminal with `print('response_label')`. 

```
font = cv2.FONT_HERSHEY_PLAIN
frame = cv2.putText(frame, '{}'.format(resp_label), (25, 35), font, 3, (255, 255, 0), 1, cv2.LINE_AA)
```
>The first line of code set the font type which the text will be written with using this constant `cv2.FONT_HERSHEY_PLAIN`. While on the second line the `cv2.putText()` method is used to write text on the video frame, and takes in nine arguments which includes the video frame `frame` the text to be displayed which in this case is the response label give by `'{}'.format(resp_label)`, the distace from the top left position where the text will be displayed which is given by `(25, 35)`, the font which is `font`, the text size in points which is `3` in this case, the color space value in RGB give by `(255, 255, 0)` how bold the text should be in points which is `1` in this case, and the kind of line which in this case is `cv2.LINE_AA` which is anti-aliased line which looks great for curves.

```
out.write(frame)  
```
>This method above is used to write each video frame. It takes one argument which is the video frame **frame**.

```
if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```
>The if statement above only execute if the keyboard key **"q"** is press. When the key is press the code breaks out of the loop. The `cv.waitKey(1)` method listens for key press and `ord('q')` is an python method that return an integer representing the Unicode code point of the character. the **0xFF** is used for case where the code is ran on a 64 bit machine.

```
 else:
        break
```
>The else code block only breaks the loop if the **valid** variable as a boolean value of 0.

```
cap.release()
out.release()
```
>The `cap.release()` and `out.release()` method closes video file or capturing device.
---

### scene_recognition_api_from_video_to_display.py
<div id="11"></div>

```
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
```
__Code break down__ 

```
import numpy as np
import cv2
import requests
```
> The three lines of code above is used to import **numpy** which is python numerical library on the first line, on the second line we imported opencv a computer vision library as **cv2**, and on line three we imported **request** which is a python library used for communicating with deepstack.

```
cap = cv2.VideoCapture('furious.mp4')
```
> The code above is the **VideoCapture()** method is used by opencv to read a video file, and it takes in the file to be read as argument. In this case it is **furious.mp4**.

```
progress_tracker = 0
response_label = ""
skip_frame = 20
```
> The three lines of code above is used to declare **progress_tracker** variable on the first line. On the second line we declare the **response_label** which is stores the scene label returned by Deepstack. On the third line we declare **skip_frame** variable which store the amount of frames to be skipped before scene detection is performed by deepstack. If you want the scene detection to be performed on every frame use the value of 1.

```
while(cap.isOpened()):
```
> In the line of code above we have **cap.isOpened()** which return the boolean value of 1 if the video capture as been initialized. The **while** loop will continue to run while the boolean value is 1.

```
valid, frame = cap.read()
```
>In the line of code above we have **cap.read()** which returns two values a bolean which can either 1 or 0 depend on if a video frame has been read or not, and the boolean values are stored in the **valid** variable. The second value returned by **cap.read()** is the video frame which is then stored in the **frame** variable.

```
if valid == True:
        progress_tracker += 1
```
>If **valid** on the first line has a boolean value of 1 the **if** code block below the will be executed. on the second line the **progress_tracker** variable will be incremented by 1.


```
if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/scene",
                                                        files={"image":new_frame}).json()
            response_label = response['label']
            print(response_label)
```
>The first line of code `if(progress_tracker % skip_frame == 0)` checks if required number of video frames have been skipped then the code block in the **if** statement will be executed. On the second line we have `retval, new_frame = cv2.imencode('.jpg', frame)` and here the **cv2.imencode('.jpg', frame)** method compresses the video frame stored with **frame** argument into a memory buffer which is then passed to the **new_frame**. This method also takes in parameter like **.jpg** which is the extension that discribes the output format. On the third line we have `response = requests.post("http://localhost:80/v1/vision/detection", files={"image":`**new_frame** `}).json()` that send a post request to the deepstack AI server, and the response a saved in the **response** variable. On the fourth line the `response['label']` are store into the `response_label` variable. On the fifth line the response label that contains the label returned by deepstack object_dectection API are been printed on the terminal with `print('response_label')`. 

```
font = cv2.FONT_HERSHEY_PLAIN
frame = cv2.putText(frame, '{}'.format(resp_label), (25, 35), font, 3, (255, 255, 0), 1, cv2.LINE_AA)
```
>The first line of code set the font type which the text will be written with using this constant `cv2.FONT_HERSHEY_PLAIN`. While on the second line the `cv2.putText()` method is used to write text on the video frame, and takes in nine arguments which includes the video frame `frame` the text to be displayed which in this case is the response label give by `'{}'.format(resp_label)`, the distace from the top left position where the text will be displayed which is given by `(25, 35)`, the font which is `font`, the text size in points which is `3` in this case, the color space value in RGB give by `(255, 255, 0)` how bold the text should be in points which is `1` in this case, and the kind of line which in this case is `cv2.LINE_AA` which is anti-aliased line which looks great for curves.

```
cv2.imshow('Image Viewer', frame)
```
>This method above display each video frame. It takes two argument the name of the view port window **'Image Viewer'** and the video frame **frame**.

```
if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```
>The if statement above only execute if the keyboard key **q** is press. When the key is press the code breaks out of the loop. The `cv.waitKey(1)` method listens for key press and `ord('q')` is an python method that returns an integer representing the Unicode code point of the character. The **0xFF** is used for case where the code is ran on a 64 bit machine.

```
 else:
        break
```
>The else code block only breaks the loop if the **valid** variable as a boolean value of 0.

```
cap.release()
cv2.destroyAllWindows()
```
>The `cap.release()` method closes video file or capturing device. while the `cv2.destroyAllWindows()` method destroys all the view port windows that were created.
---

### scene_recognition_api_from_video_to_file.py
<div id="12"></div>

```
import cv2
import numpy as np
import requests


cap = cv2.VideoCapture('furious.mp4')
out = cv2.VideoWriter("scene_recognition_from_video_to_file.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                                    24,((int(cap.get(3)), int(cap.get(4)))))

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
        out.write(frame)        
        
    else:
        break

print('<==============Video file as been full written with face bounding boxes============>')

cap.release()
out.release()
```
__Code break down__ 

```
import numpy as np
import cv2
import requests
```
> The three lines of code above is used to import **numpy** which is python numerical library on the first line, on the second line we imported opencv a computer vision library as **cv2**, and on line three we imported **request** which is a python library used for communicating with deepstack.

```
cap = cv2.VideoCapture('furious.mp4')
```
> The code above is the **VideoCapture()** method is used by opencv to read a video file, and it takes in the file to be read as argument. In this case it is **furious.mp4**.

```
out = cv2.VideoWriter("face_detection_from_camera_to_file.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24,((int(cap.get(3)), int(cap.get(4)))))

```
>The code above we have the `VideoWriter()` method which is used for writing videos. This method takes in four arguments which are the name the video will be save as `"face_detection_from_camera_to_file.avi"`, the codec for saving the video which is done with `cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')` method, the numbers of fames to save as per seconds; in this case we are saving at `24` frames per second. The last argument is the dimension for which the video is to be saved given by this `((int(cap.get(3)), int(cap.get(4)))))`, the `cap.get(3)` and `cap.get(4)` method returns the horizontal and vertical dimension of the capture video frames.

```
progress_tracker = 0
response_label = ""
skip_frame = 20
```
> The three lines of code above is used to declare **progress_tracker** variable on the first line. On the second line we declare the **response_label** which is stores the scene label returned by Deepstack. On the third line we declare **skip_frame** variable which store the amount of frames to be skipped before scene detection is performed by deepstack. If you want the scene detection to be performed on every frame use the value of 1.

```
while(cap.isOpened()):
```
> In the line of code above we have **cap.isOpened()** which return the boolean value of 1 if the video capture as been initialized. The **while** loop will continue to run while the boolean value is 1.

```
valid, frame = cap.read()
```
>In the line of code above we have **cap.read()** which returns two values a bolean which can either 1 or 0 depend on if a video frame has been read or not, and the boolean values are stored in the **valid** variable. The second value returned by **cap.read()** is the video frame which is then stored in the **frame** variable.

```
if valid == True:
        progress_tracker += 1
```
>If **valid** on the first line has a boolean value of 1 the **if** code block below the will be executed. on the second line the **progress_tracker** variable will be incremented by 1.


```
if(progress_tracker % skip_frame == 0):
            retval, new_frame = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:80/v1/vision/scene",
                                                        files={"image":new_frame}).json()
            response_label = response['label']
            print(response_label)
```
>The first line of code `if(progress_tracker % skip_frame == 0)` checks if required number of video frames have been skipped then the code block in the **if** statement will be executed. On the second line we have `retval, new_frame = cv2.imencode('.jpg', frame)` and here the **cv2.imencode('.jpg', frame)** method compresses the video frame stored with **frame** argument into a memory buffer which is then passed to the **new_frame**. This method also takes in parameter like **.jpg** which is the extension that discribes the output format. On the third line we have `response = requests.post("http://localhost:80/v1/vision/detection", files={"image":`**new_frame** `}).json()` that send a post request to the deepstack AI server, and the response a saved in the **response** variable. On the fourth line the `response['label']` are store into the `response_label` variable. On the fifth line the response label that contains the label returned by deepstack object_dectection API are been printed on the terminal with `print('response_label')`. 

```
font = cv2.FONT_HERSHEY_PLAIN
frame = cv2.putText(frame, '{}'.format(resp_label), (25, 35), font, 3, (255, 255, 0), 1, cv2.LINE_AA)
```
>The first line of code set the font type which the text will be written with using this constant `cv2.FONT_HERSHEY_PLAIN`. While on the second line the `cv2.putText()` method is used to write text on the video frame, and takes in nine arguments which includes the video frame `frame` the text to be displayed which in this case is the response label give by `'{}'.format(resp_label)`, the distace from the top left position where the text will be displayed which is given by `(25, 35)`, the font which is `font`, the text size in points which is `3` in this case, the color space value in RGB give by `(255, 255, 0)` how bold the text should be in points which is `1` in this case, and the kind of line which in this case is `cv2.LINE_AA` which is anti-aliased line which looks great for curves.

```
out.write(frame)  
```
>This method above is used to write each video frame. It takes one argument which is the video frame **frame**.

```
if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```
>The if statement above only execute if the keyboard key **"q"** is press. When the key is press the code breaks out of the loop. The `cv.waitKey(1)` method listens for key press and `ord('q')` is an python method that return an integer representing the Unicode code point of the character. the **0xFF** is used for case where the code is ran on a 64 bit machine.

```
 else:
        break
```
>The else code block only breaks the loop if the **valid** variable as a boolean value of 0.

```
print('<==============Video file as been full written with labels============>')
```
>This line of code print `'<==============Video file as been full written with labels============>'` to the terminal telling the user that the video as been full written with labels.

```
cap.release()
out.release()
```
>The `cap.release()` and `out.release()` method closes video file or capturing device.
---



```python

```
