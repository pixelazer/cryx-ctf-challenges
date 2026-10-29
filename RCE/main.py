'''
This file is part of a challenge for CRYX CTF [SPHINX 2026]
Written by Aryan Takalkar.
'''

from flask import Flask, request, render_template
from subprocess import run as runProcess
from platform import system

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    current_os = system()
    content="No file opened"

    if request.method == "POST":
        file_id = request.form.get("file_id", "").strip()

        if current_os == "Linux" or current_os == "Darwin":
            content = runProcess(
                f"cat ./static/{file_id}",
                shell = True,
                capture_output = True,
                text = True
            )

        elif current_os == "Windows":
            content = runProcess(
                f"type \"./static/{file_id}\"",
                shell = True,
                capture_output = True,
                text = True
            )

    return(render_template("index.html", content=content.stdout))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
