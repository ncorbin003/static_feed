from flask import Flask, render_template, Response
import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", 'supersekrit')
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")
ip_url=os.environ.get('IP_URL')


@app.route("/login")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    return render_template("streamer.html", value=ip_url)


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/streamer")
def streamer():
    return render_template("streamer.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
