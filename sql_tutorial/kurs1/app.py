from flask import Flask,render_template,flash,url_for,request,flash,g
from datetime import datetime
import os
import sys
from author import Author
from cantor_offer import CantorOffer
import sqlite3


app=Flask(__name__) 
app.config["SECRET_KEY"]="123goniszty"
app_info={'db_cantor'
          :r'C:\Users\bNicewicz\Desktop\python\flask-mobilo-udemy-main\sql_tutorial\data\cantors.db'
          ,'db_notifications':
          r'C:\Users\bNicewicz\Desktop\python\flask-mobilo-udemy-main\sql_tutorial\data\notifications.db'}

def get_db():
    if not hasattr(g,'sqlite_db'):
        connection=sqlite3.connect(app_info["db_cantor"])
        connection.row_factory=sqlite3.Row
        g.sqlite_db=connection
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

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
            amount='100' 
        
        if 'amount' in request.form:
            amount=request.form['amount']
        elif offer.get_by_code(currency)=='unknown':
            flash(f"Selected currency: {currency} is unknown and can not be accepted")
        else:
            db=get_db()
            sql_command="insert into transactions(currency,amount,user) values(?,?,?)"
            db.execute(sql_command,[currency,amount,'admin'])
            db.commit()
            print(currency,amount)
            flash(f"Request to exchange {currency} was accepted")        
        
        
        return render_template("exchange_results.html"
                            ,currency=currency
                            ,amount=amount
                            ,currency_info=offer.get_by_code(currency))
@app.route("/columns_grid")
def columns_grid():
    return render_template("columns.html")
if __name__=="__main__":
    app.run(port=5003)