from flask import Flask, render_template, Response
import cv2
#from time import time

app = Flask(__name__)

camera = cv2.VideoCapture(0)
camera.set(3, 448)  # 640
camera.set(4, 336)  # 480

print("hello")


def gen_frames():  
    # prev_t = 0
    # curr_t = 0 
    while True:
        success, frame = camera.read()  # read the camera frame
        # curr_t = time()
        # fps = 1 / (curr_t - prev_t)
        # prev_t = curr_t
        #frame = cv2.putText(frame, f"{fps} fps", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 2, cv2.LINE_AA)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/')
def index():
    return 'Hello world'

@app.route("/test1")
def test1():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False, port=5001)