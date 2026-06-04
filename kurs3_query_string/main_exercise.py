from flask import Flask,request
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
    font_size=20
    if 'font-size' in request.args:
        font_size=request.args['font-size']
    body = f'''<h1 style="font-size:{font_size}">\
        In the receipt {receipt} \
        you are on step {step}</H1>''' 
    return  body 

if __name__=="__main__":
    app.run()