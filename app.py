
import streamlit as st
import qrcode, csv, os
from PIL import Image
import zxingcpp
from sklearn.tree import DecisionTreeClassifier

st.title("AI QR Attendance")

roll = st.text_input("Roll Number")
if st.button("Generate QR") and roll:
    qr = qrcode.make(roll)
    st.image(qr)
    qr.save("student.png")

img = st.file_uploader("Upload QR", type=["png", "jpg", "jpeg"])
if img and st.button("Mark Attendance"):
    codes = zxingcpp.read_barcodes(Image.open(img).convert("RGB"))
    if codes:
        with open("attendance.csv", "a", newline="") as f:
            csv.writer(f).writerow([codes[0].text, "Present"])
        st.success("Attendance marked!")

ai = DecisionTreeClassifier()
ai.fit([[90], [80], [60], [40]], [0, 0, 1, 1])
p = st.number_input("Attendance %", 0, 100, 75)

if st.button("AI Prediction"):
    st.write("Low attendance risk" if ai.predict([[p]])[0] else "Attendance OK")

if os.path.exists("attendance.csv"):
    st.write("Attendance Records")
    st.dataframe(__import__("pandas").read_csv("attendance.csv", header=None))

