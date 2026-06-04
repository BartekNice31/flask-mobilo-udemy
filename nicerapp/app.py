from flask import Flask,render_template,url_for,request,flash
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
import os
import sys
load_dotenv(r".flaskenv") 
app=Flask(__name__) 
bootstrap=Bootstrap(app)

@app.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
    app.run()