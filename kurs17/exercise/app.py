from flask import Flask,render_template
from dotenv import load_dotenv
import os
import pathlib
load_dotenv(r"C:\Users\Bartłomiej\Desktop\python\flask-mobilo-udemy-main\.flaskenv")

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__=='__main__':
    app.run()