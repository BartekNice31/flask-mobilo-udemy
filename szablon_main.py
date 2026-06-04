from flask import Flask
from dotenv import load_dotenv
import os
import sys
load_dotenv(r".flaskenv")

app=Flask(__name__)

@app.route("/")
def route():
    return "<h1>Hello from python</h1>" 

if __name__=="__main__":
    app.run()