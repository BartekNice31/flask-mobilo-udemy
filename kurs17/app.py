from flask import Flask,render_template,flash,url_for 
from datetime import datetime
import os
import sys
from author import Author

app=Flask(__name__)
#bootstrap=Bootstrap(app=app)

@app.route("/")
def index():
    return render_template("index.html",time_now=datetime.now(),author=f"@{Author()}")

if __name__=="__main__":
    app.run()