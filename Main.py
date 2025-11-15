from flask import Flask, request, redirect, url_for, render_template
from datetime import datetime
import os

app = Flask(__name__)

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
        posts.insert(0, {
            "user": user,
            "content": content,
            "image_url": image_url,
            "time": datetime.now().strftime("%H:%M")
        })

    return redirect(url_for("index", user=user))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
