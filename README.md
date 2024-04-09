Smart attendace system uses face recognition to mark the attendace of people visibile in the camera and sends an email to of their attendance being noted as present.

### Pre-requisites
1. opencv-python
2. face_recognition
3. numpy
4. pandas
5. smtp & smtplib
6. threading

### Algorithm
1. Detection of faces of humans and recognises the same.
   - Requires us to creat a folder named images and upload the picture of all the persons along with their names to be detected
2. Based on the input video, whenever a person is detected, the face encodings of the detected person is compared with the face encodings of the picture.
3. if the encoding matches, the persons name is inputted in a csv file along with the time which can be viewed in Attendance.csv
4. Using smtp library the detected person's mail_id is fetched and their attendance record is sent. A seperate 'mail_class.py' file is uploaded and respective changes can be done there as per requirements.
5. The mail status is noted in output.csv

### Testing
Run python face_recognition.py
