'''
This file is part of a challenge for CRYX CTF [SPHINX 2026]
Written by Aryan Takalkar
'''

from flask import Flask, request, render_template

app = Flask(__name__)


FILES = {
    "TrustMeLol": "getDuped",
    "readme.txt": "Project archive: CRYX CTF SPHINX 2026\nOwner: challenge team\nStatus: ready for review",
    "server.log": "[2026-10-26 18:42:11] Application started on port 5000",
    "config.json": '{"theme": "default", "debug": false, "version": "1.0.0"}',
    "backup-2026-10-25.zip": "Backup created successfully. No errors reported.",
    "public-notes": "Remember to remove temporary files before deployment.",
    "": "",
    "YThmM2syeDlxN3B3": "CRYX{MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCB}"
}


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        file_id = request.form.get("file_id", "").strip()
        message = FILES.get(file_id, "File not found.")

    return render_template("index.html", message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
