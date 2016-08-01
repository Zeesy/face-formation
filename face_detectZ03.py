#based on
#http://www.mindsensors.com/blog/how-to/how-to-install-opencv-on-raspberry-pi-and-do-face-tracking

#TO DO:
#detect faces on low-resolution feed (124x160), export onto unmodified hi-res feed (1080x1920)
#blur face detect (top layer) or layer feeds

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import imutils

# Get user supplied values
cascPath = sys.argv[1]

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# initialize the *first* camera and grab a reference to the raw camera capture
cameraHI = PiCamera()
cameraHI.resolution = (720, 1280)
cameraHI.framerate = 24
rawCapture = PiRGBArray(cameraHI, size=(720, 1280))

# allow the camera to warmup
time.sleep(0.1)
lastTime = time.time()*1000.0

# initialize the *second* camera and grab a reference to the raw camera capture
cameraLO = PiCamera()
cameraLO.resolution = (90, 160)
cameraLO.framerate = 24
rawCapture = PiRGBArray(cameraLO, size=(90, 160))

# allow the camera to warmup
time.sleep(0.1)
lastTime = time.time()*1000.0


# capture frames from the *first* camera
for frame in cameraHI.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
	# clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
        
  
# capture frames from the *second* camera
for frame in cameraLO.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.CASCADE_SCALE_IMAGE
    )
    print time.time()*1000.0-lastTime," Found {0} faces!".format(len(faces))
    lastTime = time.time()*1000.0
    # Draw a circle around the faces
    for (x, y, w, h) in faces:
        cv2.circle(image, (x+w/2, y+h/2), int((w+h)/3), (255, 255, 255), 1)
    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
        

