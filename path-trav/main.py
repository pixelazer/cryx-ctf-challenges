'''
This file is part of a challenge for CRYX CTF [SPHINX 2026]
Written by Aryan Takalkar.
'''

from flask import Flask, request, render_template
from pathlib import Path

HOME_DIR = Path(__file__).resolve().parent
STATICS = HOME_DIR / "static"
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    content = "No file selected."
    files = [file for file in (STATICS / 'docs').iterdir()]

    if request.method == "POST":
        file_id = request.form.get("file_id", "").strip()

        if len(file_id) < 1:
            return(render_template("index.html", content="No file selected.", files=files))

        try:
            tgt : Path = (STATICS / 'docs' / file_id).resolve()

            if tgt.is_relative_to(STATICS):
                if tgt.is_file():
                    content = tgt.read_text(errors='replace')
                    files = [file for file in tgt.parent.iterdir()]

                else:
                    files = [file for file in tgt.iterdir()]
            else:
                print(tgt)
                content = "Access denied."

        except FileNotFoundError:
            tgt = STATICS / 'docs'
            content = "Could not find the file specified."

    return(render_template("index.html", content=content, files=files))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)