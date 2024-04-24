from flask import Flask, render_template, Response, request
import cv2
import numpy as np

app = Flask(__name__)
camera = None  # Placeholder for the camera object

def process_frame(frame):
    detector=cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('Haarcascades/haarcascade_eye.xml')
    faces=detector.detectMultiScale(frame,1.1,7)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    return frame


def gen_frames():
    global camera
    if camera is None:
        return

    while True:
        success, frame = camera.read()  # Read the camera frame
        if not success:
            break
        else:
            frame = process_frame(frame)  # Process the frame for face recognition
            ret, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )


@app.route("/")
def index():
    return render_template("./index.html")


@app.route("/video_feed", methods=["POST"])
def video_feed():
    global camera
    if "stream" not in request.files:
        return "No video stream uploaded", 400

    # Read the video stream from the request
    video_stream = request.files["stream"]
    camera = cv2.VideoCapture(video_stream)

    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)
