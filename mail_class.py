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
import pandas as pd


class EmailThread(Thread):
    def __init__(self, email_to):
        self.email_to = email_to
        Thread.__init__(self)

    def run(self):
        body = "You are under my surveillance"
        text = "your plain body"
        message = MIMEMultipart("alternative")
        message["Subject"] = "subject"
        message["From"] = "#########@gmail.com"
        message["To"] = self.email_to
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(body, "html")
        message.attach(part1)
        message.attach(part2)
        # print(self.email_to)
        # print(message)
        server = smtplib.SMTP_SSL("smtp.gmail.com", ###)
        server.login("#########@gmail.com", '###############')
        server.sendmail("##########@gmail.com", self.email_to, message.as_string())
        print('mail sent')
        csv_input = pd.read_csv('Attendance.csv')
        csv_input['mail_details'] = 'mail sent'
        csv_input.to_csv('output.csv', index=False)


def mark_attendance(name):
    with open('Attendance.csv', 'r+') as f:
        my_data_list = f.readlines()[1:]
        namelist = []
        for line in my_data_list:
            entry = line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now = datetime.now()
            dt_string = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dt_string}')
            mail_dict = {'name': 'mail_id', ...}#input the name of the person and their mail_id
            for i in mail_dict:
                if i == name:
                    email_to = str(mail_dict[i])
                    print(email_to)
                    print(name)
                    obj = EmailThread(email_to)
                    obj.run()









