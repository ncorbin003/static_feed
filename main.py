
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, Response
from sys import stdout
import cv2
import os
import redis
import gevent
from flask import Flask, redirect, url_for
from flask_socketio import SocketIO, emit
from camera import Camera
from flask_dance.contrib.github import make_github_blueprint, github
from utils import base64_to_pil_image, pil_image_to_base64



app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", 'supersekrit')
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")
camera = Camera()

@app.route("/login")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    return render_template("streamer.html")


def gen():
    """Video streaming generator function."""

    app.logger.info("starting to generate frames!")
    while True:
        frame = camera.get_frame() #pil_image_to_base64(camera.get_frame())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def index():
   return render_template("index.html")



@app.route("/streamer")
def streamer():
    return render_template("streamer.html")



if __name__ == '__main__':
    app.run(debug = True,host="0.0.0.0",port=8000)
