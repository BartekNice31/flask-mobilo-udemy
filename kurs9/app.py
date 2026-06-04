from flask import Flask,render_template,url_for,request
from dotenv import load_dotenv
import os
import sys
load_dotenv(r".flaskenv")

app=Flask(__name__)

@app.route("/")
def route():
    return "<h1>Hello from python</h1>" 

@app.route("/exchange",methods=["GET","POST"])
def exchange():
    if request.method=="GET":
        return render_template("exchange.html")
    else:
        currency='EUR'
        amount='100'
        if 'currency' in request.form:
            currency=request.form['currency']
        if 'amount' in request.form:
            amount=request.form['amount']
        return render_template("exchange_results.html",currency=currency,amount=amount)
if __name__=="__main__":
    app.run()