import numpy as np
import cv2
import threading

#from importlib import import_module  # not used
import os
from flask import Flask, render_template, Response  # refactor to fastapi
from multiprocessing import Process, Manager
import time


app = Flask(__name__)

camera = cv2.VideoCapture(0)


def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
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


# @app.route('/temp')
# def index():
#     return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def test_img():
    camera = cv2.VideoCapture(0)

    camera.set(3, 640)
    camera.set(4, 480)

    width = int(camera.get(3))
    height = int(camera.get(4))

    M = cv2.getRotationMatrix2D((width / 2, height / 2), 180, 1)
    camera.set(cv2.CAP_PROP_BUFFERSIZE,1)
    cv2.setUseOptimized(True)

    _, img = camera.read()

    print("img:")
    print(type(img))
    print(img.shape)

    cv2.imwrite("img_test.png", img)
    cv2.imwrite("img_test.jpg", img)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')