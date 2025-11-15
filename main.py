from flask import Flask, request, redirect, url_for, render_template
from flask_socketio import SocketIO
from datetime import datetime
import os

app = Flask(__name__)

# WebSocket server
socketio = SocketIO(app, cors_allowed_origins="*")

# Simple in-memory feed
posts = []


@app.route("/", methods=["GET"])
def index():
    user = request.args.get("user", "Guest")
    return render_template("index.html", posts=posts, current_user=user)


@app.route("/post", methods=["POST"])
def add_post():
    user = (request.form.get("user") or "Guest").strip() or "Guest"
    content = (request.form.get("content") or "").strip()
    image_url = (request.form.get("image_url") or "").strip()

    if content:
        post = {
            "user": user,
            "content": content,
            "image_url": image_url,
            "time": datetime.now().strftime("%H:%M"),
        }
        # خزّنه في الذاكرة
        posts.insert(0, post)
        # ابعثه فوراً لكل المتصفحات المفتوحة
        socketio.emit("new_post", post, broadcast=True)

    # الشخص اللي كتب البوست يرجع لصفحته عادي
    return redirect(url_for("index", user=user))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    # نستخدم SocketIO server بدل app.run
    socketio.run(app, host="0.0.0.0", port=port)
