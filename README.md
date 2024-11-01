# Smart-Election-System

![OpenCV](https://img.shields.io/badge/OpenCV-4.x-blue) ![Django](https://img.shields.io/badge/Django-3.x-green) ![Python](https://img.shields.io/badge/Python-3.x-yellow) ![License](https://img.shields.io/badge/license-MIT-brightgreen)

The **Smart Election System** is a secure voting platform that uses face recognition for voter authentication, minimizing fraud and enhancing the efficiency of the election process. This system is built using **Django**, **OpenCV**, and the **K-Nearest Neighbors (KNN)** algorithm.

## Features

- **Secure Voter Authentication**: Uses face recognition to ensure only registered voters can participate.
- **Real-Time Face Capture**: Webcam support to capture live images for authentication.
- **User Registration with Face Data**: Registers voters with face data stored securely.
- **Efficient Voting Process**: Streamlined authentication for a quick voting process.

## Tech Stack

- **Backend**: Django
- **Face Recognition**: OpenCV and K-Nearest Neighbors (KNN) Algorithm
- **Programming Language**: Python

## Project Structure

```plaintext
smart-election-system/                       
├── smartelection/                    # Django project folder
│   ├── app/                          # Main app folder
│   │   ├── migrations/               # Django migrations
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── Assets/                       # Assets for the project
│   │   └── background.png            # Background image
│   ├── data/                         # Data folder for face recognition
│   │   ├── faces_data.pkl            # Serialized face data
│   │   └── names.pkl                 # Serialized names data
│   ├── static/smartelection/         # Static files for the project
│   │   ├── img1.jpg
│   │   └── img2.png
│   ├── Templates/                    # HTML Templates
│   │   ├── Home.html                 # Home page template
│   │   └── Register.html             # Registration page template
│   ├── db.sqlite3                    # SQLite database file
│   ├── manage.py                     # Django management script
│   └── Votes.csv                     # CSV file to store voting records
└── requirements.txt                  # Project dependencies
