import cv2
from flask import Flask, render_template, Response, request

indx = "0"
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/show/", methods=["POST"])
def action():
    global indx
    global video_capture
    indx = request.form["indx"]
    if indx == "1":
        print("cam 1")
        video_capture = cv2.VideoCapture(0)

    elif indx == "2":
        print("cam 2")
        video_capture = cv2.VideoCapture(2)
    return render_template("index.html")


def gen_frames_null():
    print("gen_frames_null")
    with open("templates/image1.jpg", "rb") as img:
        frame = img.read()
    while True:
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


def gen_frames():
    global video_capture
    while True:
        success, frame = video_capture.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed")
def video_feed():
    global indx
    print(indx)
    if indx != "0":
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(
            gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
        )
    else:
        return Response(
            gen_frames_null(), mimetype="multipart/x-mixed-replace; boundary=frame"
        )


if __name__ == "__main__":
    app.run()
