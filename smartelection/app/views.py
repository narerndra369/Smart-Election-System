from django.shortcuts import render
import cv2
import face_recognition
import pickle
import numpy as np
import os
import csv
import time
import uuid
from sklearn.neighbors import KNeighborsClassifier
from datetime import datetime
from win32com.client import Dispatch

# Constants
DATA_DIR = 'data/'
COL_NAMES = ["Name", "Vote", "Date", "Timestamp"]

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def speak(message):
    """Use Windows Text-to-Speech to provide audio feedback."""
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(message)

def home(request):
    """Home view."""
    return render(request, 'Home.html')

def homeregister(request):
    """Home redirect Registration Page."""
    return render(request, 'Register.html')

def register(request):
    """Register new face data for voting."""

    video = cv2.VideoCapture(0)
    facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces_data = []
    
    if request.method=="POST":
        print(request.method)
        name=request.POST.get('usern')
        print("name",name)
        i = 0
        framesTotal = 51
        captureAfterFrame = 2
        # Capture frames
        while True:
            ret, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                crop_img = frame[y:y+h, x:x+w]
                resized_img = cv2.resize(crop_img, (50, 50))
                
                # Capture frames at specified intervals
                if len(faces_data) < framesTotal and i % captureAfterFrame == 0:
                    faces_data.append(resized_img)
                
                i += 1
                cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)

            cv2.imshow('frame', frame)
            k = cv2.waitKey(1)
            if k == ord('q') or len(faces_data) >= framesTotal:
                break

        video.release()
        cv2.destroyAllWindows()

        # Convert faces_data to numpy array and reshape
        faces_data = np.asarray(faces_data)
        faces_data = faces_data.reshape((framesTotal, -1))
        print(faces_data)

        # Handle names data
        if 'names.pkl' not in os.listdir('data/'):
            names = [name] * framesTotal
            with open('data/names.pkl', 'wb') as f:
                pickle.dump(names, f)
        else:
            with open('data/names.pkl', 'rb') as f:
                names = pickle.load(f)
            names.extend([name] * framesTotal)  # Append names
            with open('data/names.pkl', 'wb') as f:
                pickle.dump(names, f)

        # Handle faces_data
        if 'faces_data.pkl' not in os.listdir('data/'):
            with open('data/faces_data.pkl', 'wb') as f:
                pickle.dump(faces_data, f)
        else:
            with open('data/faces_data.pkl', 'rb') as f:
                faces = pickle.load(f)
            faces = np.append(faces, faces_data, axis=0)  # Append new faces data
            with open('data/faces_data.pkl', 'wb') as f:
                pickle.dump(faces, f)
        message = "Registration successful!"
        message_type = "success"  # Could also be "danger", "warning", etc.
        return render(request, 'Home.html', {"message": message,"message_type": message_type})

def check_if_exists(value):
    try:
        with open("Votes.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0] == value:
                    return True
    except FileNotFoundError:
        print("File not found or unable to open the CSV file.")
    return False


def givevote(request):
    video = cv2.VideoCapture(0)
    facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if not os.path.exists('data/'):
        os.makedirs('data/')
    try:
        with open('data/names.pkl', 'rb') as f:
            LABELS = pickle.load(f)
    except (FileNotFoundError, pickle.UnpicklingError) as e:
        print("Error loading names.pkl:", e)
        LABELS = []
    # Load face data
    try:
        with open('data/faces_data.pkl', 'rb') as f:
            FACES = pickle.load(f)
    except (FileNotFoundError, pickle.UnpicklingError) as e:
        print("Error loading faces_data.pkl:", e)
        FACES = np.empty((0, 2500))  # Create an empty array for faces
    
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(FACES, LABELS)
    vote_options = {'1': 'BJP', '2': 'CONGRESS', '3': 'AAP', '4': 'NOTA'}
    imgBackground = cv2.imread(r"C:\Users\nare6\OneDrive\Desktop\SmartElectionSystem\smartelection\Assets\background.png")

    while True:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)

        output = None  # Initialize output to a default value
        for (x, y, w, h) in faces:
            crop_img = frame[y:y+h, x:x+w]
            resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
            output = knn.predict(resized_img)
            ts = time.time()
            date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
            timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
            exist = os.path.isfile("Votes.csv")
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
            cv2.putText(frame, str(output[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

            attendance = [output[0], timestamp]

        imgBackground[370:370 + 480, 225:225 + 640] = frame
        cv2.imshow('frame', imgBackground)
        k = cv2.waitKey(1)
        message,message_type='',''
        if output is not None:
            voter_exist = check_if_exists(output[0])
            if voter_exist:
                speak("YOU HAVE ALREADY VOTED")
                message = "YOU HAVE ALREADY VOTED"
                message_type = "warning"  # Could also be "danger", "warning", etc.
                break
                print("Already VOted")
                

            if k == ord('1'):
                speak("YOUR VOTE HAS BEEN RECORDED")
                time.sleep(5)
                if exist:
                    with open("Votes.csv", "a") as csvfile:
                        writer = csv.writer(csvfile)
                        attendance = [output[0], "BJP", date, timestamp]
                        writer.writerow(attendance)
                else:
                    with open("Votes.csv", "a") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(COL_NAMES)
                        attendance = [output[0], "BJP", date, timestamp]
                        writer.writerow(attendance)
                speak("THANK YOU FOR PARTICIPATING IN THE ELECTIONS")
                break

            if k == ord('2'):
                speak("YOUR VOTE HAS BEEN RECORDED")
                time.sleep(5)
                if exist:
                    with open("Votes.csv", "a") as csvfile:
                        writer = csv.writer(csvfile)
                        attendance = [output[0], "CONGRESS", date, timestamp]
                        writer.writerow(attendance)
                else:
                    with open("Votes.csv", "a") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(COL_NAMES)
                        attendance = [output[0], "CONGRESS", date, timestamp]
                        writer.writerow(attendance)
                speak("THANK YOU FOR PARTICIPATING IN THE ELECTIONS")
                break

            if k == ord('3'):
                speak("YOUR VOTE HAS BEEN RECORDED")
                time.sleep(5)
                if exist:
                    with open("Votes.csv", "a") as csvfile:
                        writer = csv.writer(csvfile)
                        attendance = [output[0], "AAP", date, timestamp]
                        writer.writerow(attendance)
                else:
                    with open("Votes.csv", "a") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(COL_NAMES)
                        attendance = [output[0], "AAP", date, timestamp]
                        writer.writerow(attendance)
                speak("THANK YOU FOR PARTICIPATING IN THE ELECTIONS")
                break

            if k == ord('4'):
                speak("YOUR VOTE HAS BEEN RECORDED")
                time.sleep(5)
                if exist:
                    with open("Votes.csv", "a") as csvfile:
                        writer = csv.writer(csvfile)
                        attendance = [output[0], "NOTA", date, timestamp]
                        writer.writerow(attendance)
                else:
                    with open("Votes.csv", "a") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(COL_NAMES)
                        attendance = [output[0], "NOTA", date, timestamp]
                        writer.writerow(attendance)
                message = "THANK YOU FOR PARTICIPATING IN THE ELECTIONS"
                message_type = "success"  # Could also be "danger", "warning", etc.
                speak("THANK YOU FOR PARTICIPATING IN THE ELECTIONS")
                break
    video.release()
    cv2.destroyAllWindows()
    return render(request, 'Home.html', {"message": message,"message_type": message_type})
                
                
    

