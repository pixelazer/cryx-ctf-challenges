'''
This file is part of a challenge for CRYX CTF [SPHINX 2026]
Written by Aryan Takalkar.
'''

from flask import Flask, request, render_template
from subprocess import run as runProcess, TimeoutExpired

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    content="Enter text..."

    if request.method == "POST":
        arg = request.form.get("input_text", "").strip()

        if arg == "": return(render_template("index.html", content=content))

        command = f"echo -n {arg} | sha256sum"

        try:
            content = runProcess(
                command,
                shell = True,
                capture_output = True,
                text = True,
                # preexec_fn = limit_resources,   # crashes the app if used
                timeout = 3
            )
        except TimeoutExpired:
            content = "Request timed out."
        except OSError:
            content = "Request failed to execute."


    return(render_template("index.html", content=content))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
