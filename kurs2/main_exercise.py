from flask import Flask
from dotenv import load_dotenv
import os
import sys
load_dotenv(r".flaskenv")

app=Flask(__name__)

@app.route("/")
def route():
    return "<h1>Hello from main route</h1>"

@app.route('/cook/<string:receipt>/<int:step>') 
def cook(receipt, step): 
    body = f'''<H1>In the receipt {receipt} you are on step {step}</H1>''' 
    return  body 

if __name__=="__main__":
    app.run()