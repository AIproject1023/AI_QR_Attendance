import qrcode, cv2, csv
from sklearn.tree import DecisionTreeClassifier

roll = input("Enter roll number: ")
qrcode.make(roll).save("student.png")

# Scan QR code
cam = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

while True:
    ok, img = cam.read()
    if not ok:
        break
    data, _, _ = detector.detectAndDecode(img)
    cv2.imshow("Scan QR", img)
    if data:
        cam.release()
        cv2.destroyAllWindows()
        break
    if cv2.waitKey(1) == 27:
        cam.release()
        cv2.destroyAllWindows()
        raise SystemExit

# Save attendance
with open("attendance.csv", "a", newline="") as f:
    csv.writer(f).writerow([data, "Present"])

# Simple machine learning model
model = DecisionTreeClassifier()
model.fit([[90], [80], [60], [40]], [0, 0, 1, 1])

attendance = int(input("Attendance percentage: "))
result = model.predict([[attendance]])[0]

print("Attendance marked for:", data)
print("AI prediction:", "Low attendance risk" if result == 1 else "Attendance OK")
