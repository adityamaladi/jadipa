# WEB library
import streamlit.components.v1 as components
from secrets import choice
import streamlit as st

# opencv library
import face_recognition
from datetime import datetime
from PIL import Image
import pandas as pd
import numpy as np
import cv2
import os
import time

FRAME_WINDOW = st.image([])  # frame window

hide_st_style = """ 
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)  # hide streamlit menu

path = 'Images_Attendance'
images = []
classNames = []
myList = os.listdir(path)
#print(myList)

menu = ["HOME", "PRESENSI","DATA", "ABOUT"]  # menu
choice = st.sidebar.selectbox("Menu", menu)  # sidebar menu

col1, col2, col3 = st.columns(3)  # columns
cap = cv2.VideoCapture(0)  # capture video
if choice == 'PRESENSI':
    st.markdown("<h2 style='text-align: center; color: black;'>AMBIL DAFTAR HADIR</h2>",
                unsafe_allow_html=True)  # title
    with col1:  # column 1
        st.subheader("PRESENSI")
        run = st.checkbox("MULAI PRESENSI")  # checkbox
    if run == True:
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        print(classNames)

        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        def markAttendance(name):
            with open ('Attendance.csv','r+')as f:
                myDataList = f.readlines()
                # print(myDataList)
                nameList = []
                for line in myDataList:
                    entry = line.split(',')
                    # print(entry[0])
                    nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    tString = now.strftime('%d:%m:%Y')
                    dtString = now.strftime('%H:%M:%S')
                    f.writelines(f'\n{name},{dtString},{tString}')

        encodeListKnown = findEncodings(images)
        print('Encoding Complete')
        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()
            # img = captureScreen()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                # print(name)
                # else: name = "unknown"
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)
            FRAME_WINDOW.image(img)
            cv2.waitKey(1)
    else:
        pass

elif choice == 'DATA':
    with col2:
        df = pd.read_csv('Attendance.csv')
        st.subheader("HASIL PRESENSI")
        df = pd.read_csv('Attendance.csv')
        st.write(df)

        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')
        my_large_df = pd.read_csv('Attendance.csv')
        csv = convert_df(my_large_df)
        now = datetime.now()
        tString = now.strftime('%d:%m:%Y')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f'Presensi Kelas/{tString}',
            mime='text/csv',
        )
elif choice == 'HOME':
    with st.container():
            st.title("Presensi Otomatis")
            st.subheader('Bagaimana Menggunakannnya?')
            st.write('##')
            st.write(
                """
                - Pastikan Device yang anda gunakan sudah terkoneksi dengan CCTV melalui jaringan Wifi.
                - Masuk ke menu NAV BAR di pojok kiri atas, kemudian pilih menu "PRESENSI".
                - Untuk memulai presensi, tekan CHECKBOX "MULAI PRESENSI ". 
                - Untuk melihat hasil presensi, pergi ke menu NAV BAR dan klik bagian "DATA".
                - Untuk mendowload hasil presensi, klik "DOWLOAD SEBAGAI CSV".
                """)

        # st.image("Images_Attendance/adit.jpg",
        #          width=990, caption="MY wife")


