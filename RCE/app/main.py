'''
This file is part of a challenge for CRYX CTF [SPHINX 2026]
Written by Aryan Takalkar.
'''

from flask import Flask, request, render_template
from subprocess import run as runProcess, TimeoutExpired

# AI CONTENT
def limit_resources():
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))          # 30 CPU-seconds max
    resource.setrlimit(resource.RLIMIT_NPROC, (30, 30))       # max 10 processes — kills fork bombs
    resource.setrlimit(resource.RLIMIT_AS, (100 * 1024 * 1024, 100 * 1024 * 1024))  # 100MB address space
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))  # 1MB max file writes

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
                preexec_fn = limit_resources,   # AI CONTENT
                timeout = 3
            )
        except TimeoutExpired:
            content = "Request timed out."
        except OSError:
            content = "Request failed to execute."


    return(render_template("index.html", content=content))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
