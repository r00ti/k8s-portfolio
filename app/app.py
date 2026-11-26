import os
import socket

from flask import Flask, jsonify

app = Flask(__name__)

VERSION = os.environ.get("APP_VERSION", "0.2.0")
state = {"live": True, "ready": True}

ITEMS = [
    {"id": 1, "name": "first item"},
    {"id": 2, "name": "second item"},
]


@app.get("/health/live")
def live():
    if state["live"]:
        return jsonify(status="alive")
    return jsonify(status="broken"), 500


@app.get("/health/ready")
def ready():
    if state["ready"]:
        return jsonify(status="ready")
    return jsonify(status="not ready"), 503


@app.post("/admin/<probe>/<mode>")
def toggle(probe, mode):
    if probe not in state or mode not in ("on", "off"):
        return jsonify(error="use /admin/<live|ready>/<on|off>"), 400
    state[probe] = mode == "on"
    return jsonify(state)


@app.get("/version")
def version():
    return jsonify(version=VERSION, pod=socket.gethostname())


@app.get("/items")
def items():
    return jsonify(ITEMS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
