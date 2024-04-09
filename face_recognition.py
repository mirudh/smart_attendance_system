import cv2
import time
import face_recognition
import numpy as np
from datetime import datetime
import smtp
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pickle
import csv
import mail_class


class WebcamStream:
    # initialization method
    def __init__(self, stream_id=0):
        self.stream_id = stream_id  # default is 0 for main camera

        # opening video capture stream
        self.vcap = cv2.VideoCapture(self.stream_id)
        if self.vcap.isOpened() is False:
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        fps_input_stream = int(self.vcap.get(5))  # hardware fps
        print("FPS of input stream: {}".format(fps_input_stream))

        # reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.vcap.read()
        if self.grabbed is False:
            print('[Exiting] No more frames to read')
            exit(0)
        # self.stopped is initialized to False
        self.stopped = True
        # thread instantiation
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True  # daemon threads run in background

    # method to start thread
    def start(self):
        self.stopped = False
        self.t.start()

    # method passed to thread to read next available frame
    def update(self):
        while True:
            if self.stopped is True:
                break
            self.grabbed, self.frame = self.vcap.read()
            if self.grabbed is False:
                print('[Exiting] No more frames to read')
                self.stopped = True
                break
        self.vcap.release()

    # method to return latest read frame
    def read(self):
        return self.frame

    # method to stop reading frames
    def stop(self):
        self.stopped = True


with open('filename.bin', 'rb') as handle:
    data = pickle.load(handle)

webcam_stream = WebcamStream(stream_id=0)   # 0 id for main camera
webcam_stream.start()
# processing frames in input stream
num_frames_processed = 0
start = time.time()
while True:
    if webcam_stream.stopped is True:
        break
    else:
        img = webcam_stream.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(data, encodeFace)
            faceDis = face_recognition.face_distance(data, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                Name = smtp.classNames[matchIndex]
                print(Name)
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 2), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, Name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                mail_class.mark_attendance(Name)

    delay = 0.03
    time.sleep(delay)
    num_frames_processed += 1
    cv2.imshow('frame', img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

end = time.time()
webcam_stream.stop()  # stop the webcam stream

# printing time elapsed and fps
elapsed = end-start
fps = num_frames_processed/elapsed












