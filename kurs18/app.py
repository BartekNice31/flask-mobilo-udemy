from flask import Flask,render_template,flash,url_for,request,flash
from datetime import datetime
import os
import sys
from author import Author
from cantor_offer import CantorOffer
app=Flask(__name__) 
app.config["SECRET_KEY"]="123goniszty"

@app.route("/")
def index():
    return render_template("index.html",time_now=datetime.now(),author=f"@{Author()}")
@app.route("/exchange",methods=["GET","POST"])
def exchange():
    offer=CantorOffer()
    offer.load_offer()
    
    if request.method=="GET":
        
        return render_template("exchange.html",offer=offer)
    else:
        flash("LOAD OFFER")
        flash("Debug starting exchange in POST mode")
        currency='EUR'
        if 'currency' in request.form:
            currency=request.form['currency']
        if currency in offer.denies_codes:
            flash(f"Selected currency: {currency} can not be accepted")
        elif offer.get_by_code(currency)=='unknown':
            flash(f"Selected currency: {currency} is unknown and can not be accepted")
        else:
            flash(f"Request to exchange {currency} was accepted")        
        
        amount='100' 
        
        if 'amount' in request.form:
            amount=request.form['amount']
        return render_template("exchange_results.html"
                            ,currency=currency
                            ,amount=amount
                            ,currency_info=offer.get_by_code(currency))
if __name__=="__main__":
    app.run()