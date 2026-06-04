from flask import Flask,render_template,url_for,request
from dotenv import load_dotenv
import os
import sys
load_dotenv(r".flaskenv")
from currency import Currency
from cantor_offer import CantorOffer
app=Flask(__name__)

@app.route("/")
def route():
    return "<h1>Hello from python</h1>" 

@app.route("/exchange",methods=["GET","POST"])
def exchange():
    offer=CantorOffer()
    offer.load_offer()

    if request.method=="GET":
        return render_template("exchange.html",offer=offer)
    else:
        currency='EUR'
        amount='100' 
        if 'currency' in request.form:
            currency=request.form['currency']
        if 'amount' in request.form:
            amount=request.form['amount']
        return render_template("exchange_results.html"
                            ,currency=currency
                            ,amount=amount
                            ,currency_info=offer.get_by_code(currency))
if __name__=="__main__":
    app.run()