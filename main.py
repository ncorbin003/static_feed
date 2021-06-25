# from functools import wraps
# import json
# from os import environ as env
# from werkzeug.exceptions import HTTPException
#
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, Response
# from flask import jsonify
# from flask import redirect
# from flask import session
from flask import url_for, redirect
# from authlib.integrations.flask_client import OAuth
# from six.moves.urllib.parse import urlencode
#
# import constants
import cv2
import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", 'supersekrit')
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")

camera = cv2.VideoCapture(0)


@app.route("/login")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    return "You are @{login} on GitHub".format(login=resp.json()["login"])


def gen_frames():
    while True:
        #success: a bool data type, returns true if Python is able to read the VideoCapture() object
        #frame: a numpy array, represents the first image that the video captures
        #read(): returns a bool. If frame is read correctly, it will be True
        success, frame = camera.read()
        if not success:
            break
        else:
            #cv2.imencode(): function is to convert(encode) the image format into streaming data and assign it to
            # memory cache. it is mainly used for compressing image data format to facilitate network transmission
            #yield keyword: lets the execution to continue and keeps on generating frame until alive
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/video_feed")
def video_feed():
   return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
   app.run(debug = True)
