from flask import Flask,render_template,flash,url_for
from flask_bootstrap import Bootstrap
from datetime import datetime
import os
import sys

app=Flask(__name__)
bootstrap=Bootstrap(app=app)

@app.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
    app.run()