from flask import Flask
from dotenv import load_dotenv
import os
load_dotenv(r".flaskenv")

app=Flask(__name__)

@app.route("/")
def route():
    return "<h1>Hello from python</h1>"

@app.route("/cantor/<currency>/<amount>")
def cantor(currency:int,amount:int):
    print(currency,amount)
    
if __name__=="__main__":
    app.run()