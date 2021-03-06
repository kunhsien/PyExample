#https://stackoverflow.com/questions/33650974/opencv-python-read-specific-frame-using-videocapture?newreg=2495db9d80934aa3b199f6d8d7489f89
#opencv for python3 => http://www.lfd.uci.edu/~gohlke/pythonlibs/
#video guide : https://www.youtube.com/watch?v=ulJdZn0qBCQ
import matplotlib
import numpy as np
import cv2

#Get video name from user
#Ginen video name must be in quotes, e.g. "pirkagia.avi" or "plaque.avi"
video_name = input("Please give the video name including its extension. E.g. \"pirkagia.avi\":\n")

#Open the video file
cap = cv2.VideoCapture(video_name)

#Set frame_no in range 0.0-1.0
#In this example we have a video of 30 seconds having 25 frames per seconds, thus we have 750 frames.
#The examined frame must get a value from 0 to 749.
#For more info about the video flags see here: https://stackoverflow.com/questions/11420748/setting-camera-parameters-in-opencv-python
#Here we select the last frame as frame sequence=749. In case you want to select other frame change value 749.
#BE CAREFUL! Each video has different time length and frame rate.
#So make sure that you have the right parameters for the right video!
time_length = 30.0
fps=25
frame_seq = 749
frame_no = (frame_seq /(time_length*fps))

#The first argument of cap.set(), number 2 defines that parameter for setting the frame selection.
#Number 2 defines flag CV_CAP_PROP_POS_FRAMES which is a 0-based index of the frame to be decoded/captured next.
#The second argument defines the frame number in range 0.0-1.0
cap.set(2,frame_no);

#Read the next frame from the video. If you set frame 749 above then the code will return the last frame.
ret, frame = cap.read()

#Set grayscale colorspace for the frame.
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#Cut the video extension to have the name of the video
my_video_name = video_name.split(".")[0]

#Display the resulting frame
cv2.imshow(my_video_name+' frame '+ str(frame_seq),gray)

#Set waitKey
cv2.waitKey()

#Store this frame to an image
cv2.imwrite(my_video_name+'_frame_'+str(frame_seq)+'.jpg',gray)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



#Displaying a webcam feed using OpenCV and Python
#https://stackoverflow.com/questions/2601194/displaying-a-webcam-feed-using-opencv-and-python

#How do I access my webcam in Python?
#https://stackoverflow.com/questions/604749/how-do-i-access-my-webcam-in-python

#OPENCV Python 使用webcam錄影 http://opencv123.blogspot.tw/2015/07/opencv-python-webcam.html

#Open Webcam using OpenCV on Python https://ccw1986.blogspot.tw/2015/07/opencvpython-open-webcam-using-opencv.html

#OpenCV/Python: read specific frame using VideoCapture
#https://stackoverflow.com/questions/33650974/opencv-python-read-specific-frame-using-videocapture?newreg=2495db9d80934aa3b199f6d8d7489f89

#Install OpenCV 3 with Python 3 on Windows
#https://www.solarianprogrammer.com/2016/09/17/install-opencv-3-with-python-3-on-windows/

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")