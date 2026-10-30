'''
This file is part of a challenge for CRYX CTF [SPHINX 2026]
Written by Aryan Takalkar.
'''

from flask import Flask, request, render_template
from subprocess import run as runProcess, TimeoutExpired
from platform import system

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    current_os = system()
    content="Enter text..."

    if request.method == "POST":
        arg = request.form.get("input_text", "").strip()

        if arg == "": return(render_template("index.html", content=content))

        if current_os == "Linux" or current_os == "Darwin":
            command = f"echo -n \"{arg}\" | sha256sum"

        elif current_os == "Windows":
            command = f"echo {arg} | certutil -hashfile - SHA256"

        try:
            content = runProcess(
                command,
                shell = True,
                capture_output = True,
                text = True,
                timeout = 5
            )
        except TimeoutExpired:
            content = "Request timed out."


    return(render_template("index.html", content=content))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
