from os import listdir
from flask import Flask
from flask import render_template
import json


app = Flask(__name__)


@app.route('/')
def playlist():
    with open('metadata.json', 'r') as f:
        articles = json.load(f)
        return render_template("./playlist.html", articles=articles)

if __name__ == "__main__":
    app.run(debug=True)
