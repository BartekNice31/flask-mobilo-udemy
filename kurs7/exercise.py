from flask import Flask,request,redirect,url_for
from dotenv import load_dotenv
import os
import sys
load_dotenv(r".flaskenv")

app=Flask(__name__)

@app.route("/")
def index():
    menu=f'''<h1>Hello from python</h1> 
    <br><p>Click <a href="{url_for('new_receipt')}">here</a> to new receipt page</p>
    <br><p>Click <a href="{url_for("delete_receipt")}">here</a> to delete receipt page</p>
    '''    
    return menu

@app.route("/not_implemented/<string:message>")
def not_implemented(message:str):
    body=f'<h1>{message}</h1>'
    return body
    
@app.route("/new_receipt")
def new_receipt():
    # return "<h1>NEW RECEIPT</h1>"
    return redirect(url_for('not_implemented',message='Function new_receipt is not ready yet'))

@app.route("/delete_receipt")
def delete_receipt():
    return redirect(url_for('not_implemented',message='Function delete_receipt is not ready yet'))

if __name__=="__main__":
    app.run()